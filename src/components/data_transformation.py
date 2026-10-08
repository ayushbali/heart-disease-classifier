from dataclasses import dataclass
from pathlib import Path
import os
from numpy import median
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

import joblib

# DATA TRANSFORMATION

# 1. Load train and test data
# 2. Validation - missing, duplicates, etc
# 3. split into features and targets
# 4. Encode categorical columns
# 5. Scale numerical columns

@dataclass
class DataTransformationConfig:
  project_root:Path = Path(__file__).resolve().parents[2]
  preprocessor_path = project_root / "artifacts" / "preprocessor.pkl"

  def __post_init__(self):
        self.preprocessor_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

  target_col = "target"

class DataTransformation:
  def __init__(self):
    self.config = DataTransformationConfig()
    self.preprocessor = None

  def load_data(self, train_data, test_data):
    train_df = pd.read_csv(train_data)
    test_df = pd.read_csv(test_data)

    return (train_df, test_df)

  def validation(self, train_df, test_df):
    # CHECK IF THERE ARE MISSING VALUES
    train_missing = train_df.isna().sum()
    test_missing = test_df.isna().sum()

    # CHECK IF THERE ARE ANY DUPLICATES
    train_duplicates = train_df.duplicated().sum()
    test_duplicates = test_df.duplicated().sum()

    print("Train missing values:")
    print(train_missing[train_missing > 0])

    print("Test missing values:")
    print(test_missing[test_missing > 0])

    print(f"Train duplicates: {train_duplicates}")
    print(f"Test duplicates: {test_duplicates}")

  def split_features(self, train_df, test_df):
    target_col = self.config.target_col

    # X_train, y_train
    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]

    # X_test, y_test
    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]

    return X_train, X_test, y_train, y_test

  def identify_columns(self, X_train):
    numerical_columns = X_train.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

    categorical_columns = X_train.select_dtypes(
            include=["object", "category", "string"]
      ).columns.tolist()

    return numerical_columns, categorical_columns

  def build_preprocessor(self, numerical_columns, categorical_columns):
    # Numerical Pipeline
    numerical_pipeline = Pipeline(
      steps = [("imputer", SimpleImputer(strategy="median")),
               ("scaler", StandardScaler())])
    
    categorical_pipeline = Pipeline(steps =[
      ("imputer", SimpleImputer(strategy="most_frequent")),
      ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    self.preprocessor = ColumnTransformer(transformers= 
                        [("numerical", numerical_pipeline, numerical_columns),
                     ("categorial", categorical_pipeline, categorical_columns)]
    )
    return self.preprocessor

  def transform_data(self, X_train, X_test):
    X_train_transformed = self.preprocessor.fit_transform(X_train)
    X_test_transformed = self.preprocessor.transform(X_test)

    return X_train_transformed, X_test_transformed

  def save_preprocessor(self):
    joblib.dump(self.preprocessor, self.config.preprocessor_path)