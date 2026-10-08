import os
from pathlib import Path
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

# Support both `python -m src.components.data_ingestion` and running this file
# directly from the project directory (where Python otherwise only adds
# src/components to sys.path).
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
  sys.path.insert(0, str(PROJECT_ROOT))

from src.components import data_transformation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTraining
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
# Resolve paths from the project root, independent of the launch directory.
  project_root: Path = Path(__file__).resolve().parents[2]

  raw_data_path: Path = project_root / "data" / "heart-disease.csv"
  train_data_path: Path = project_root / "data" / "train_data.csv"
  test_data_path: Path = project_root / "data" / "test_data.csv"


  # raw_data_path = os.path.join(os.getcwd(), 'data/heart-disease.csv')
  # train_data_path = os.path.join(os.getcwd(), 'data/train_data.csv')
  # test_data_path = os.path.join(os.getcwd(), 'data/test_data.csv')


  # project_root: Path = Path(__file__).resolve().parents[2]
  # train_data_path: str = str(project_root / 'artifact' / 'training_data.csv')
  # test_data_path: str = str(project_root / 'artifact' / 'test_data.csv')
  # source_data_path: str = str(project_root / 'data' / 'heart-disease.csv')


class DataIngestion:
  def __init__(self):
    self.ingestion_config = DataIngestionConfig()

  def load_data(self) -> pd.DataFrame:
    df = pd.read_csv(self.ingestion_config.raw_data_path)
    return df

  def split_data(self, df):
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42, stratify=df["target"])
    return(train_data, test_data)

  def save_data(self, train_data: pd.DataFrame, test_data: pd.DataFrame):
    self.ingestion_config.train_data_path.parent.mkdir(parents=True, exist_ok=True)
    self.ingestion_config.test_data_path.parent.mkdir(parents=True, exist_ok=True)

    train_data.to_csv(self.ingestion_config.train_data_path, index=False)
    test_data.to_csv(self.ingestion_config.test_data_path, index=False)


# if __name__ == "__main__":

#   # DATA INGESTION
#   data_ingest_obj = DataIngestion()
#   df = data_ingest_obj.load_data()
#   train_data, test_data = data_ingest_obj.split_data(df)
#   data_ingest_obj.save_data(train_data, test_data)
  
#   # DATA TRANSFORMATION
#   data_transformation = DataTransformation()
#   train_df, test_df = data_transformation.load_data(
#       data_ingest_obj.ingestion_config.train_data_path,
#       data_ingest_obj.ingestion_config.test_data_path,
#   )
#   data_transformation.validation(train_df, test_df)
#   X_train, X_test, y_train, y_test = data_transformation.split_features(train_df, test_df)

#   numerical_columns, categorical_columns = data_transformation.identify_columns(X_train)
#   data_transformation.build_preprocessor(numerical_columns, categorical_columns)
#   X_train_transformed, X_test_transformed = data_transformation.transform_data(X_train, X_test)

#   data_transformation.save_preprocessor()

#   train_array = np.c_[
#     X_train_transformed,
#     y_train.to_numpy()
# ]

#   test_array = np.c_[
#     X_test_transformed,
#     y_test.to_numpy()
#   ]

#   # MODEL TRAINING
#   model_training = ModelTraining()
#   model_training.initiate_model_training(train_array, test_array)