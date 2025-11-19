# SONAR Rock vs Mine Prediction Web App

🌊 **SonarCheck** - AI-Powered Underwater Object Detection System

![SONAR Detection](https://img.shields.io/badge/SONAR%20Classification-Rock%20vs%20Mine-blue?style=flat-square)
![ML Model](https://img.shields.io/badge/Model-XGBoost-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12-yellow?style=flat-square)

## 🎯 Features

- **Real-time Classification**: Predicts whether underwater objects are rocks or mines
- **Confidence Scoring**: Provides probability scores for each prediction (0-100%)
- **Risk Assessment**: Automated risk level determination with recommendations
- **Feature Explanation**: Shows which SONAR frequencies most influence predictions
- **REST API**: Programmatic access for integration and automation
- **Production-Ready**: Gunicorn/WSGI support, health checks, error handling

## 🏗️ Project Structure

```
sonar project/
├── app_sonar_predict.py           # Main Flask application
├── SONAR_03.ipynb                 # ML model training notebook
├── requirements.txt               # Python dependencies
├── runtime.txt                    # Python version (for deployment)
├── Procfile                       # Gunicorn start command
├── templates/
│   ├── sonar_form.html           # Input form page
│   ├── sonar_result.html         # Results visualization
│   └── sonar_about.html          # Project information
└── models/ (created after training)
    ├── best_sonar_model.pkl      # XGBoost model
    ├── logistic_regression_model.pkl
    ├── top_risk_factors.pkl
    └── feature_info.pkl
```

## 📊 Model & Data

- **ML Model**: XGBoost (primary), Logistic Regression (backup)
- **Preprocessing**: StandardScaler for feature normalization
- **Dataset**: SONAR dataset from UCI ML Repository
  - 208 samples (111 rocks, 97 mines)
  - 60 frequency bands as features
  - Binary classification task

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
Open `SONAR_03.ipynb` in Jupyter Notebook and run all cells:
```bash
jupyter notebook SONAR_03.ipynb
```

This will generate the model files in the project directory.

### 3. Run the Flask App
```bash
python app_sonar_predict.py
```

The application will start on `http://localhost:5000`

### 4. Access the Web Interface
- **Prediction Form**: http://localhost:5000/
- **API Endpoint**: POST to http://localhost:5000/api/predict
- **About Page**: http://localhost:5000/about
- **Health Check**: http://localhost:5000/health

---

## 🎓 Two Main Goals

### Goal 1: Rock vs Mine Classification
Accurately predict object type using 60 SONAR frequency bands:
- **Rock**: Natural underwater formation (low risk)
- **Mine**: Potential explosive device (high risk)
- **Confidence**: Probability score with risk level

### Goal 2: Discover Classification Factors
Identify which SONAR frequencies best distinguish objects:
- Feature importance ranking
- Top contributing frequency bands
- Signal pattern analysis

---

## 📡 SONAR Frequency Characteristics

| Frequency Range | Typical Pattern | Object Type |
|-----------------|-----------------|-------------|
| Low (0-19) | Smooth distribution | Both rock and mine |
| Mid (20-40) | Moderate peaks | Mixed signals |
| High (41-59) | Sharp peaks | Often mine signatures |

---

## 🛡️ Security & Best Practices

✅ No secrets or credentials in code
✅ Input validation and error handling
✅ Health check endpoint for monitoring
✅ Production-ready (Gunicorn support)
✅ Proper model versioning and serialization
✅ Comprehensive error messages

---

## 📈 Model Performance

- **Training Method**: 80/20 split with stratification
- **Validation**: 5-fold cross-validation
- **Optimization**: Threshold optimization for accuracy
- **Interpretation**: SHAP analysis and feature importance

---

## 🚢 Deployment

### Heroku
```bash
git add .
git commit -m "Deploy SonarCheck"
git push heroku main
```

### Render.com
- Connect GitHub repository
- Set Python 3.12.3 as runtime
- Deploy automatically

### Docker
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app_sonar_predict:app"]
```

---

## 📚 Technologies Used

- **Backend**: Python 3.12, Flask, scikit-learn, XGBoost
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: pandas, numpy
- **Model Serialization**: joblib
- **Server**: Gunicorn (WSGI)

---

## ⚠️ Important Disclaimer

**SonarCheck is for research and educational purposes only.** This system should NOT be used as the sole basis for real-world maritime safety decisions. Always consult with qualified professionals and follow established naval protocols.

---

## 👨‍💻 Development Notes

### Model Training Process
1. Load SONAR data from CSV
2. Exploratory Data Analysis (EDA)
3. Feature preprocessing (StandardScaler)
4. Train XGBoost and backup LogisticRegression models
5. Cross-validation and threshold optimization
6. Feature importance analysis
7. Model serialization for deployment

### API Usage Example
```python
import requests

data = {
    'frequency_values': [0.02, 0.04, 0.05, ...] # 60 values
}

response = requests.post(
    'http://localhost:5000/api/predict',
    json=data
)

print(response.json())
```

---

## 📖 References

- **Dataset**: UCI Machine Learning Repository - SONAR Dataset
- **XGBoost**: https://xgboost.readthedocs.io/
- **Flask**: https://flask.palletsprojects.com/
- **scikit-learn**: https://scikit-learn.org/

---

## 👥 Authors & Credits

### Project Development

- **Repository Owner**: [Abdullah Al Noman](https://github.com/nomanrafi)
- **Project Name**: SONAR Rock vs Mine Prediction
- **Developed**: 2025

### Framework & Technology Credits

#### Machine Learning Libraries

- **scikit-learn**: Pedregosa et al. (2011) - Scikit-learn: Machine Learning in Python
- **XGBoost**: Chen & Guestrin (2016) - XGBoost: A Scalable Tree Boosting System
- **pandas**: McKinney (2010) - Data Analysis with pandas
- **numpy**: Harris et al. (2020) - Array programming with NumPy

#### Web Framework

- **Flask**: Ronacher (2010) - Flask: A Python Microframework
- **Jinja2**: Template engine used by Flask

#### Data Visualization & Analysis

- **matplotlib**: Hunter (2007) - Matplotlib: A 2D Graphics Environment
- **seaborn**: Waskom et al. - Seaborn: Statistical Data Visualization

#### Deployment & DevOps

- **Gunicorn**: Weiss (2010) - Gunicorn: Python WSGI HTTP Server
- **Docker**: Docker Inc. - Container Platform
- **Heroku**: Cloud Platform for Deployment

### Dataset Attribution

#### UCI Machine Learning Repository

- **Authors**: Gorman, R.P. and Sejnowski, T.J. (1988)
- **Dataset**: Connectionist Bench (Sonar, Mines vs. Rocks)
- **URL**: [https://archive.ics.uci.edu/ml/datasets/Connectionist+Bench+%28Sonar%2C+Mines+vs+Rocks%29](https://archive.ics.uci.edu/ml/datasets/Connectionist+Bench+%28Sonar%2C+Mines+vs+Rocks%29)

### Community & Resources

- **Stack Overflow**: Community support and solutions
- **GitHub**: Open-source community contributions
- **Kaggle**: Dataset exploration and community insights
- **Machine Learning Mastery**: Best practices and tutorials

### Special Thanks

- Open source community for excellent tools and libraries
- UCI Machine Learning Repository for quality datasets
- Flask and scikit-learn communities for comprehensive documentation
- All contributors who provided feedback and improvements

---

## 📝 License Information

This project utilizes open-source libraries and datasets. Please refer to individual library licenses:

- scikit-learn: BSD License
- XGBoost: Apache License 2.0
- Flask: BSD License
- pandas: BSD License
- numpy: BSD License

The UCI SONAR dataset is publicly available under the Creative Commons License.

---

## 🙏 Contributing

We welcome contributions! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit pull requests
4. Report issues and suggestions
5. Improve documentation

### How to Contribute

- **Bug Reports**: Open an issue with detailed description
- **Feature Requests**: Suggest improvements via issues
- **Code Contributions**: Submit PRs with clear descriptions
- **Documentation**: Help improve README and comments

---

**Built with ❤️ using Python & Machine Learning**

Special appreciation to all open-source developers and the ML community!
