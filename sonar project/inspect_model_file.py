import joblib
import sys
import os

output_file = r"d:\git\GitHub\SONAR-Rock-vs-Mine-Prediction - Copy\sonar project\model_inspection.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    try:
        base_path = r"d:\git\GitHub\SONAR-Rock-vs-Mine-Prediction - Copy\sonar project\models"
        model_path = os.path.join(base_path, 'best_sonar_model.pkl')
        
        f.write(f"Loading model from: {model_path}\n")
        if not os.path.exists(model_path):
            f.write("Model file not found!\n")
        else:
            model = joblib.load(model_path)
            f.write(f"Model Type: {type(model)}\n")
            
            if hasattr(model, 'steps'):
                f.write("Model is a Pipeline. Steps:\n")
                for name, step in model.steps:
                    f.write(f"  - {name}: {type(step)}\n")
            else:
                f.write("Model is NOT a Pipeline.\n")
                
        # Check backup model
        backup_path = os.path.join(base_path, 'logistic_regression_model.pkl')
        if os.path.exists(backup_path):
            f.write(f"\nLoading backup model from: {backup_path}\n")
            backup = joblib.load(backup_path)
            f.write(f"Backup Model Type: {type(backup)}\n")
            if hasattr(backup, 'steps'):
                f.write("Backup Model is a Pipeline. Steps:\n")
                for name, step in backup.steps:
                    f.write(f"  - {name}: {type(step)}\n")
            else:
                f.write("Backup Model is NOT a Pipeline.\n")

    except Exception as e:
        f.write(f"Error: {e}\n")
