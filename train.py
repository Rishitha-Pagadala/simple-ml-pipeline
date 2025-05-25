import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import joblib # For saving the model
import os

# Define a directory to save the model
MODEL_DIR = "/app/model" # This path will be inside the Docker container
MODEL_PATH = os.path.join(MODEL_DIR, "iris_model.joblib")

def train_model():
    print("Loading data...")
    iris = load_iris()
    X, y = iris.data, iris.target
    X_df = pd.DataFrame(X, columns=iris.feature_names)
    y_s = pd.Series(y, name="target")

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X_df, y_s, test_size=0.2, random_state=42)

    print("Training model...")
    model = LogisticRegression(max_iter=200) # Increased max_iter for convergence
    model.fit(X_train, y_train)

    print(f"Model accuracy: {model.score(X_test, y_test)}")

    # Ensure model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"Saving model to {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)
    print("Model saved successfully!")

if __name__ == "__main__":
    train_model()