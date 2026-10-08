import joblib
import os
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

class PredictionPipeline:
    def __init__(self):
        self.model_path = project_root / "artifacts" / "model" / "model.pkl"
        self.preprocessor_path = project_root / "artifacts" / "preprocessor.pkl"

        self.model = self.load_model()
        self.preprocessor = self.load_preprocessor()

    def load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
        model = joblib.load(self.model_path)
        return model

    def load_preprocessor(self):
        if not self.preprocessor_path.exists():
            raise FileNotFoundError(f"Preprocessor file not found at {self.preprocessor_path}")
        preprocessor = joblib.load(self.preprocessor_path)
        return preprocessor

    def predict(self, features: pd.DataFrame):
        
        transformed_features = self.preprocessor.transform(features)
        predictions = self.model.predict(transformed_features)
        
        return predictions


class CustomData:

    def __init__(
        self,
        age: int,
        sex: int,
        cp: int,
        trestbps: int,
        chol: int,
        fbs: int,
        restecg: int,
        thalach: int,
        exang: int,
        oldpeak: float,
        slope: int,
        ca: int,
        thal: int
    ):
        self.age = age
        self.sex = sex
        self.cp = cp
        self.trestbps = trestbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.slope = slope
        self.ca = ca
        self.thal = thal
  
    def get_data_as_dataframe(self):
        data = {
            "age": [self.age],
            "sex": [self.sex],
            "cp": [self.cp],
            "trestbps": [self.trestbps],
            "chol": [self.chol],
            "fbs": [self.fbs],
            "restecg": [self.restecg],
            "thalach": [self.thalach],
            "exang": [self.exang],
            "oldpeak": [self.oldpeak],
            "slope": [self.slope],
            "ca": [self.ca],
            "thal": [self.thal]
        }
        return pd.DataFrame(data)


# TESTING
# custom_data = CustomData(
#     age=55,
#     sex=1,
#     cp=1,
#     trestbps=140,
#     chol=250,
#     fbs=0,
#     restecg=1,
#     thalach=150,
#     exang=0,
#     oldpeak=1.2,
#     slope=1,
#     ca=0,
#     thal=2
# )

# df = custom_data.get_data_as_dataframe()
# print(df)
# pipeline = PredictionPipeline()
# predictions = pipeline.predict(df)
# print(f"Predictions: {predictions}")
