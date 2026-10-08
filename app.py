from fastapi import FastAPI
from pydantic import BaseModel
from src.pipe.prediction_pipeline import PredictionPipeline, CustomData

from fastapi.middleware.cors import CORSMiddleware

# Initialize the prediction pipeline
predict_pipeline = PredictionPipeline()

app = FastAPI(
  title="Heart Disease Prediction API",
  description="API for predicting heart disease based on patient data.",
  version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HeartDiseaseInput(BaseModel):
  age: int
  sex: int
  cp: int
  trestbps: int
  chol: int
  fbs: int
  restecg: int
  thalach: int
  exang: int
  oldpeak: float
  slope: int
  ca: int
  thal: int

@app.get('/')
def home():
  return {"message": "Welcome to the Heart Disease Prediction API!"}

@app.post('/predict')
def predict(input_data: HeartDiseaseInput):
  # Create a CustomData instance from the input data
  custom_data = CustomData(
    age=input_data.age,
    sex=input_data.sex,
    cp=input_data.cp,
    trestbps=input_data.trestbps,
    chol=input_data.chol,
    fbs=input_data.fbs,
    restecg=input_data.restecg,
    thalach=input_data.thalach,
    exang=input_data.exang,
    oldpeak=input_data.oldpeak,
    slope=input_data.slope,
    ca=input_data.ca,
    thal=input_data.thal
  )
  # Create a DataFrame from the input data
  features = custom_data.get_data_as_dataframe()
  # Make predictions
  predictions = predict_pipeline.predict(features)
  # Return the predictions as a response
  prediction = predictions[0]  # Assuming a single prediction for a single input

  if int(prediction) == 0:
    result_message = "The patient is not likely to have heart disease."
  else:
    result_message = "The patient is likely to have heart disease."
  return {
          "prediction": f"{int(prediction)}",
          "message": result_message
      }

