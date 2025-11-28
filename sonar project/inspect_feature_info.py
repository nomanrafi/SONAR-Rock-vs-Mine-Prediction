import joblib
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    path = r"d:\git\GitHub\SONAR-Rock-vs-Mine-Prediction - Copy\sonar project\models\feature_info.pkl"
    if os.path.exists(path):
        info = joblib.load(path)
        print(f"Feature Info Type: {type(info)}")
        print(f"Content: {info}")
    else:
        print("File not found")
except Exception as e:
    print(f"Error: {e}")
