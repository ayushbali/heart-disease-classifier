# model_training.py

from dataclasses import dataclass
from pathlib import Path

import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
  accuracy_score,
  precision_score,
  recall_score,
  f1_score,
)

# ============================================================
# MODEL TRAINER CONFIGURATION
# ============================================================

@dataclass
class ModelTrainerConfig:
  project_root: Path = Path(__file__).resolve().parents[2]

  model_file_path: Path = (
    project_root / "artifacts" / "model" / "model.pkl"
  )


# ============================================================
# MODEL TRAINING
# ============================================================

class ModelTraining:

  def __init__(self):
      self.config = ModelTrainerConfig()

      # Models we want to train
      self.models = {
          "Logistic Regression": LogisticRegression(max_iter=1000),
          "KNN": KNeighborsClassifier(),
          "Random Forest": RandomForestClassifier(random_state=42),
      }

  # --------------------------------------------------------
  # Train and evaluate models
  # --------------------------------------------------------

  def train_and_evaluate(self, train_array, test_array):

      # ----------------------------------------------------
      # 1. Separate X and y
      # ----------------------------------------------------

      X_train = train_array[:, :-1]
      y_train = train_array[:, -1]

      X_test = test_array[:, :-1]
      y_test = test_array[:, -1]

      # ----------------------------------------------------
      # 2. Store model evaluation results
      # ----------------------------------------------------

      model_scores = {}

      # ----------------------------------------------------
      # 3. Train and evaluate every model
      # ----------------------------------------------------

      for name, model in self.models.items():

          # Train model
          model.fit(X_train, y_train)

          # Make predictions
          y_pred = model.predict(X_test)

          # Calculate evaluation metrics
          accuracy = accuracy_score(y_test, y_pred)

          precision = precision_score(
              y_test,
              y_pred,
              zero_division=0
          )

          recall = recall_score(
              y_test,
              y_pred,
              zero_division=0
          )

          f1 = f1_score(
              y_test,
              y_pred,
              zero_division=0
          )

          # Store scores
          model_scores[name] = {
              "accuracy": accuracy,
              "precision": precision,
              "recall": recall,
              "f1": f1,
          }

      return model_scores

  # --------------------------------------------------------
  # Select best model
  # --------------------------------------------------------

  def select_best_model(self, model_scores):

      # Select model with highest F1 score
      best_model_name = max(
          model_scores,
          key=lambda name: model_scores[name]["f1"]
      )

      best_model = self.models[best_model_name]

      print(f"\nBest Model: {best_model_name}")
      print(f"F1 Score: {model_scores[best_model_name]['f1']:.4f}")

      return best_model_name, best_model

  # --------------------------------------------------------
  # Save model
  # --------------------------------------------------------

  def save_model(self, model):

      # Create directory if it doesn't exist
      self.config.model_file_path.parent.mkdir(
          parents=True,
          exist_ok=True
      )

      # Save trained model
      joblib.dump(
          model,
          self.config.model_file_path
      )

      print(
          f"\nModel saved at: "
          f"{self.config.model_file_path}"
      )

  # --------------------------------------------------------
  # Main model-training pipeline
  # --------------------------------------------------------

  def initiate_model_training(self, train_array, test_array):

      # 1. Train and evaluate all models
      model_scores = self.train_and_evaluate(
          train_array,
          test_array
      )

      # 2. Print model performance
      print("\nModel Performance:")

      for name, scores in model_scores.items():

          print(f"\n{name}")
          print(f"Accuracy : {scores['accuracy']:.4f}")
          print(f"Precision: {scores['precision']:.4f}")
          print(f"Recall   : {scores['recall']:.4f}")
          print(f"F1 Score : {scores['f1']:.4f}")

      # 3. Select best model
      best_model_name, best_model = self.select_best_model(
          model_scores
      )

      # 4. Save best model
      self.save_model(best_model)

      # 5. Return useful information
      return {
          "best_model_name": best_model_name,
          "best_model": best_model,
          "model_scores": model_scores,
      }


# ============================================================
# TESTING
# ============================================================

