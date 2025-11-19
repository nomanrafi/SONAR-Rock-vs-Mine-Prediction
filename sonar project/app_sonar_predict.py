from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
import sys
from pathlib import Path
import warnings

# Ensure UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sonar_rock_mine_prediction_2024'

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).resolve().parent
print(f"📍 Application directory: {SCRIPT_DIR}")

# ==========================================
# 1. LOAD MODELS AND PREPROCESSORS
# ==========================================

def load_models():
    """Load trained models and preprocessing objects"""
    try:
        # Get absolute paths for model files
        model_path = SCRIPT_DIR / 'best_sonar_model.pkl'
        backup_model_path = SCRIPT_DIR / 'logistic_regression_model.pkl'
        feature_info_path = SCRIPT_DIR / 'feature_info.pkl'
        risk_factors_path = SCRIPT_DIR / 'top_risk_factors.pkl'
        
        # Check if files exist
        print(f"🔍 Checking for model files in: {SCRIPT_DIR}")
        print(f"   - best_sonar_model.pkl: {model_path.exists()} ({model_path})")
        print(f"   - logistic_regression_model.pkl: {backup_model_path.exists()}")
        print(f"   - feature_info.pkl: {feature_info_path.exists()}")
        print(f"   - top_risk_factors.pkl: {risk_factors_path.exists()}")
        
        # Check all files exist before loading
        missing_files = []
        if not model_path.exists():
            missing_files.append(str(model_path))
        if not backup_model_path.exists():
            missing_files.append(str(backup_model_path))
        if not feature_info_path.exists():
            missing_files.append(str(feature_info_path))
        if not risk_factors_path.exists():
            missing_files.append(str(risk_factors_path))
        
        if missing_files:
            print(f"❌ Missing model files:")
            for f in missing_files:
                print(f"   - {f}")
            return None
        
        print("📦 Loading model files...")
        
        # Load the main XGBoost model
        model = joblib.load(str(model_path))
        print(f"   ✓ XGBoost model loaded: {type(model).__name__}")
        
        # Load backup logistic regression model
        backup_model = joblib.load(str(backup_model_path))
        print(f"   ✓ Backup model loaded: {type(backup_model).__name__}")
        
        # Load feature information
        feature_info = joblib.load(str(feature_info_path))
        print(f"   ✓ Feature info loaded")
        
        # Load risk factors (feature importance)
        risk_factors = joblib.load(str(risk_factors_path))
        print(f"   ✓ Risk factors loaded")
        
        return {
            'model': model,
            'backup_model': backup_model,
            'feature_info': feature_info,
            'risk_factors': risk_factors
        }
    except FileNotFoundError as e:
        print(f"❌ File not found error: {e}")
        import traceback
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"❌ Unexpected error loading models: {e}")
        import traceback
        traceback.print_exc()
        return None


# Load all models at startup
MODELS = load_models()

if MODELS is None:
    print("❌ ERROR: Could not load required model files!")
    print("Expected files: best_sonar_model.pkl, logistic_regression_model.pkl, etc.")
else:
    print("✅ Models loaded successfully!")


# ==========================================
# 2. SONAR EQUIPMENT CHARACTERISTICS
# ==========================================

# Define SONAR frequency bands and their characteristics
SONAR_INFO = {
    'frequency_bands': 60,
    'frequency_range': '11.25 kHz to 100 kHz',
    'equipment': 'Goodman Tonals & Mirrorbird Standard SONAR',
    'application': 'Underwater object detection (Mine detection)',
    'signal_characteristics': {
        'low_frequencies': {'range': 'Bands 0-19', 'typical_for': 'Rock reflections'},
        'mid_frequencies': {'range': 'Bands 20-40', 'typical_for': 'Mixed signals'},
        'high_frequencies': {'range': 'Bands 41-59', 'typical_for': 'Mine signatures'}
    }
}

def assess_object_characteristics(prediction, confidence):
    """
    Provide detailed characteristics based on prediction.
    Goal 2: Explain what patterns indicate mine vs rock.
    
    Args:
        prediction (int): 0 = Rock, 1 = Mine
        confidence (float): Confidence percentage (0-100)
    
    Returns:
        dict: Detailed object characteristics
    """
    if prediction == 0:  # Rock
        characteristics = {
            'object_type': 'Rock',
            'description': 'Natural underwater rock formation',
            'typical_signals': 'Smooth, distributed reflections across frequency bands',
            'icon': '🪨',
            'risk_message': '✅ Safe - This is a natural rock formation'
        }
    else:  # Mine
        characteristics = {
            'object_type': 'Mine',
            'description': 'Likely explosive device or mine',
            'typical_signals': 'Concentrated, sharp reflections in high-frequency bands',
            'icon': '💣',
            'risk_message': '🚨 ALERT - Likely mine detected! Recommend immediate evasion.'
        }
    
    characteristics['confidence'] = confidence
    characteristics['confidence_level'] = get_confidence_level(confidence)
    
    return characteristics


def get_confidence_level(confidence):
    """Determine confidence descriptor based on percentage"""
    if confidence >= 95:
        return "Very High (95-100%)"
    elif confidence >= 80:
        return "High (80-95%)"
    elif confidence >= 65:
        return "Moderate (65-80%)"
    elif confidence >= 50:
        return "Fair (50-65%)"
    else:
        return "Low (<50%)"


# ==========================================
# 3. FEATURE ENGINEERING FOR PREDICTION
# ==========================================

def prepare_prediction_input(frequency_values):
    """
    Prepare and validate SONAR frequency data for prediction.
    
    Args:
        frequency_values (list): List of 60 frequency band values (0-1)
    
    Returns:
        tuple: (DataFrame for prediction, error message if any)
    """
    try:
        if not frequency_values or len(frequency_values) != 60:
            return None, "Must provide exactly 60 frequency band values."
        
        # Convert to numeric
        values = [float(v) for v in frequency_values]
        
        # Validate range
        for i, v in enumerate(values):
            if not (0 <= v <= 1):
                return None, f"Frequency band {i} has invalid value {v}. Must be between 0 and 1."
        
        # Create DataFrame
        features_df = pd.DataFrame([values])
        
        return features_df, None
    
    except (ValueError, TypeError) as e:
        return None, f"Invalid input: {str(e)}"


# ==========================================
# 4. PREDICTION LOGIC (Goal 1: Classify Rock vs Mine)
# ==========================================

def make_prediction(features_df):
    """
    Make rock vs mine prediction using trained model.
    
    Returns:
        dict: Prediction result with confidence and risk assessment
    """
    if MODELS is None:
        error_msg = (
            'Models not loaded. Please check system files.\n\n'
            'Troubleshooting:\n'
            '1. Ensure all .pkl files exist in the sonar project folder\n'
            '2. Check that SONAR_03.ipynb was run successfully\n'
            '3. Verify Python 3.11 is being used (conda)\n'
            '4. Check console output for model loading errors'
        )
        return {
            'success': False,
            'error': error_msg
        }
    
    try:
        # Use the model pipeline
        prediction = MODELS['model'].predict(features_df)[0]
        prediction_proba = MODELS['model'].predict_proba(features_df)[0]
        
        # Confidence as percentage (0-100%)
        # prediction_proba[0] = probability of Rock (0)
        # prediction_proba[1] = probability of Mine (1)
        
        if prediction == 0:  # Rock
            confidence = prediction_proba[0] * 100
            prediction_text = "🪨 ROCK DETECTED"
        else:  # Mine
            confidence = prediction_proba[1] * 100
            prediction_text = "💣 MINE ALERT"
        
        # Risk assessment
        if prediction == 1:  # Mine
            if confidence >= 90:
                risk_level = "CRITICAL"
                recommendation = "🚨 IMMEDIATE EVASION REQUIRED! Confidence in mine detection is critical."
            elif confidence >= 75:
                risk_level = "HIGH"
                recommendation = "⚠️  HIGH ALERT! Mine detection is probable. Recommend immediate evasion and reporting."
            else:
                risk_level = "MODERATE"
                recommendation = "🟡 CAUTION - Possible mine detected. Recommend further investigation before proceeding."
        else:  # Rock
            if confidence >= 90:
                risk_level = "SAFE"
                recommendation = "✅ SAFE - High confidence this is a natural rock. Safe to proceed."
            elif confidence >= 75:
                risk_level = "LIKELY SAFE"
                recommendation = "✅ Likely safe. This appears to be a natural formation. Exercise normal caution."
            else:
                risk_level = "UNCERTAIN"
                recommendation = "⚠️  Uncertain - Object may be rock or mine. Recommend detailed analysis."
        
        # Risk color
        if prediction == 1 and confidence >= 75:
            risk_color = "🔴"  # Critical mine
        elif prediction == 1:
            risk_color = "🟠"  # Possible mine
        elif prediction == 0 and confidence >= 90:
            risk_color = "🟢"  # Safe rock
        else:
            risk_color = "🟡"  # Uncertain
        
        return {
            'success': True,
            'prediction': prediction,
            'object_type': 'Mine' if prediction == 1 else 'Rock',
            'confidence_percent': confidence,
            'confidence_level': get_confidence_level(confidence),
            'prediction_text': prediction_text,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'risk_color': risk_color,
            'rock_probability': prediction_proba[0] * 100,
            'mine_probability': prediction_proba[1] * 100
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Prediction error: {str(e)}"
        }


# ==========================================
# 5. RISK FACTOR EXPLANATION (Goal 2: Feature Importance)
# ==========================================

def get_risk_factors():
    """
    Get top frequency bands that distinguish mines from rocks.
    Goal 2: Explain which SONAR frequencies are most important.
    
    Returns:
        list: Top risk factors with importance scores
    """
    if MODELS is None:
        return []
    
    try:
        risk_factors = MODELS['risk_factors']
        
        # Convert to list format
        factors = []
        max_importance = risk_factors.max() if len(risk_factors) > 0 else 1
        
        for rank, (freq_band, importance) in enumerate(risk_factors.items(), 1):
            percentage = (importance / max_importance) * 100 if max_importance > 0 else 0
            factors.append({
                'rank': rank,
                'frequency_band': int(freq_band),
                'importance': importance,
                'percentage': percentage
            })
        
        return factors
    
    except Exception as e:
        print(f"⚠️  Error getting risk factors: {e}")
        return []


# ==========================================
# 6. FLASK ROUTES
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page: Display prediction form (GET) or process prediction (POST).
    """
    if request.method == 'GET':
        return render_template('sonar_form.html', sonar_info=SONAR_INFO)
    
    elif request.method == 'POST':
        try:
            # Extract frequency values from form
            frequency_values = []
            for i in range(60):
                try:
                    val = float(request.form.get(f'freq_{i}', 0))
                    frequency_values.append(val)
                except ValueError:
                    pass
            
            # Validate and prepare input
            features_df, error = prepare_prediction_input(frequency_values)
            
            if error:
                return render_template('sonar_form.html', error=error, sonar_info=SONAR_INFO)
            
            # Make prediction (Goal 1)
            prediction_result = make_prediction(features_df)
            
            if not prediction_result['success']:
                error_msg = prediction_result.get('error', 'Unknown prediction error')
                return render_template('sonar_form.html', error=error_msg, sonar_info=SONAR_INFO)
            
            # Get object characteristics
            object_char = assess_object_characteristics(
                prediction_result['prediction'],
                prediction_result['confidence_percent']
            )
            
            # Get risk factors explanation (Goal 2)
            risk_factors = get_risk_factors()
            
            # Prepare result data
            result_data = {
                'object_type': prediction_result['object_type'],
                'confidence_percent': prediction_result['confidence_percent'],
                'confidence_level': prediction_result['confidence_level'],
                'prediction_text': prediction_result['prediction_text'],
                'risk_level': prediction_result['risk_level'],
                'recommendation': prediction_result['recommendation'],
                'risk_color': prediction_result['risk_color'],
                'rock_probability': prediction_result['rock_probability'],
                'mine_probability': prediction_result['mine_probability'],
                'object_char': object_char,
                'risk_factors': risk_factors,
                'sonar_info': SONAR_INFO
            }
            
            # Render result page
            return render_template('sonar_result.html', **result_data)
        
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"
            return render_template('sonar_form.html', error=error, sonar_info=SONAR_INFO)


@app.route('/about', methods=['GET'])
def about():
    """About page: Display project information."""
    return render_template('sonar_about.html', sonar_info=SONAR_INFO)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for programmatic predictions.
    Expects JSON: {'frequency_values': [array of 60 floats]}
    """
    try:
        data = request.get_json()
        
        if 'frequency_values' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: frequency_values'
            }), 400
        
        frequency_values = data['frequency_values']
        
        # Prepare input
        features_df, error = prepare_prediction_input(frequency_values)
        
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
        # Make prediction
        prediction_result = make_prediction(features_df)
        
        if not prediction_result['success']:
            return jsonify(prediction_result), 500
        
        # Get characteristics and risk factors
        object_char = assess_object_characteristics(
            prediction_result['prediction'],
            prediction_result['confidence_percent']
        )
        risk_factors = get_risk_factors()
        
        return jsonify({
            'success': True,
            'prediction': {
                'object_type': prediction_result['object_type'],
                'confidence_percent': round(prediction_result['confidence_percent'], 2),
                'confidence_level': prediction_result['confidence_level'],
                'risk_level': prediction_result['risk_level'],
                'recommendation': prediction_result['recommendation']
            },
            'probabilities': {
                'rock': round(prediction_result['rock_probability'], 2),
                'mine': round(prediction_result['mine_probability'], 2)
            },
            'characteristics': object_char,
            'top_risk_factors': risk_factors[:5]
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/risk-factors', methods=['GET'])
def api_risk_factors():
    """
    API endpoint to get top frequency bands (Goal 2).
    """
    try:
        risk_factors = get_risk_factors()
        return jsonify({
            'success': True,
            'risk_factors': risk_factors,
            'note': 'Top frequency bands that distinguish mines from rocks'
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/sonar-info', methods=['GET'])
def api_sonar_info():
    """
    API endpoint to get SONAR equipment and frequency information.
    """
    try:
        return jsonify({
            'success': True,
            'sonar_info': SONAR_INFO
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint. Verifies that models are loaded.
    """
    models_loaded = MODELS is not None
    return jsonify({
        'status': 'healthy' if models_loaded else 'unhealthy',
        'models_loaded': models_loaded,
        'application': 'SONAR Rock vs Mine Prediction',
        'endpoints': {
            'form': '/',
            'api_predict': '/api/predict (POST)',
            'risk_factors': '/api/risk-factors (GET)',
            'sonar_info': '/api/sonar-info (GET)',
            'health': '/health (GET)'
        }
    }), 200 if models_loaded else 503


# ==========================================
# 7. ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('sonar_form.html', error='Page not found.'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('sonar_form.html', error='Internal server error. Please try again.'), 500


# ==========================================
# 8. MAIN EXECUTION
# ==========================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print(" SONAR ROCK VS MINE PREDICTION - FLASK APPLICATION")
    print("=" * 70)
    print("\n Application Configuration:")
    print(f"   - Models Loaded: {MODELS is not None}")
    print(f"   - Form Route: http://localhost:5000/")
    print(f"   - API Endpoint: http://localhost:5000/api/predict")
    print(f"   - Risk Factors: http://localhost:5000/api/risk-factors")
    print(f"   - SONAR Info: http://localhost:5000/api/sonar-info")
    print(f"   - Health Check: http://localhost:5000/health")
    print("\n Goal 1: Classify underwater objects as rocks or mines")
    print(" Goal 2: Identify which SONAR frequencies best distinguish objects")
    print("\n" + "=" * 70 + "\n")
    
    # Run Flask app
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000,
        use_reloader=False
    )
