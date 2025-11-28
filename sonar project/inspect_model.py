import joblib
import sys
import os
import pandas as pd

# Set encoding for console output
sys.stdout.reconfigure(encoding='utf-8')

try:
    base_path = r"d:\git\GitHub\SONAR-Rock-vs-Mine-Prediction - Copy\sonar project\models"
    model_path = os.path.join(base_path, 'best_sonar_model.pkl')
    
    print(f"Loading model from: {model_path}")
    if not os.path.exists(model_path):
        print("Model file not found!")
    else:
        model = joblib.load(model_path)
        print(f"Model Type: {type(model)}")
        
        if hasattr(model, 'steps'):
            print("Model is a Pipeline. Steps:")
            for name, step in model.steps:
                print(f"  - {name}: {type(step)}")
        else:
            print("Model is NOT a Pipeline.")
            
    # Check backup model
    backup_path = os.path.join(base_path, 'logistic_regression_model.pkl')
    if os.path.exists(backup_path):
        print(f"\nLoading backup model from: {backup_path}")
        backup = joblib.load(backup_path)
        print(f"Backup Model Type: {type(backup)}")
        if hasattr(backup, 'steps'):
            print("Backup Model is a Pipeline. Steps:")
            for name, step in backup.steps:
                print(f"  - {name}: {type(step)}")
        else:
            print("Backup Model is NOT a Pipeline.")

except Exception as e:
    print(f"Error: {e}")
