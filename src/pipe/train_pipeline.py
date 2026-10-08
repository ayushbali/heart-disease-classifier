# IMPORTS
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTraining
import numpy as np

# MAIN
if __name__ == "__main__":

  # DATA INGESTION
  data_ingest_obj = DataIngestion()
  df = data_ingest_obj.load_data()
  train_data, test_data = data_ingest_obj.split_data(df)
  data_ingest_obj.save_data(train_data, test_data)
  
  # DATA TRANSFORMATION
  data_transformation = DataTransformation()
  train_df, test_df = data_transformation.load_data(
      data_ingest_obj.ingestion_config.train_data_path,
      data_ingest_obj.ingestion_config.test_data_path,
  )
  data_transformation.validation(train_df, test_df)
  X_train, X_test, y_train, y_test = data_transformation.split_features(train_df, test_df)

  numerical_columns, categorical_columns = data_transformation.identify_columns(X_train)
  data_transformation.build_preprocessor(numerical_columns, categorical_columns)
  X_train_transformed, X_test_transformed = data_transformation.transform_data(X_train, X_test)

  data_transformation.save_preprocessor()


# THESE TWO STEPS ARE UNNECESSARY 
# REQUIRES A FIX IN MODEL TRAINER CLASS
  train_array = np.c_[
    X_train_transformed,
    y_train.to_numpy()
]

  test_array = np.c_[
    X_test_transformed,
    y_test.to_numpy()
  ]

  # MODEL TRAINING
  model_training = ModelTraining()
  model_training.initiate_model_training(train_array, test_array)