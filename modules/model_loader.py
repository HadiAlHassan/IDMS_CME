# import joblib
# import os
# from pathlib import Path
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Define paths to the XGBoost model and vectorizer
# MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'XGBoostModel_GPU.joblib')
# VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'tfidf_vectorizer.joblib')

# # Load the XGBoost model and vectorizer
# xgb_model = joblib.load(MODEL_PATH)
# vectorizer = joblib.load(VECTORIZER_PATH)

# def read_and_transform(file):
#     """Read text from the file and transform it using the vectorizer."""
#     text = file.read()
#     file.close()
#     text_transformed = vectorizer.transform([text])
#     return text_transformed

# def predict_label(file):
#     """Predict the label for the text in the given file using XGBoost model."""
#     text_transformed = read_and_transform(file)
#     label = xgb_model.predict(text_transformed)[0]  # Assuming prediction returns a single label
#     return label

# if __name__ == "__main__":
#     # Define the path to the test file
#     current_dir = Path(__file__).resolve().parent
#     dataset_path = current_dir.parent / 'txtfiles' / 'LegalTest1.txt'

#     # Predict label
#     with dataset_path.open('r', encoding='utf-8') as file:
#         label = predict_label(file)
#         print("Predicted label:", label)


import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb
from pathlib import Path
import os

# Define paths to the model and vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'XGBoostModel_GPU.joblib')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'tfidf_vectorizer.joblib')

# Check if the model and vectorizer files exist
if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)):
    raise FileNotFoundError(f"Model file or vectorizer file not found. Check paths: {MODEL_PATH}, {VECTORIZER_PATH}")

# Load the trained model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def read_text_from_file(file_path):
    """Read text data from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def predict_label_from_file(file_path):
    """Predict the label for text data in the given file."""
    # Read text data from file
    text = read_text_from_file(file_path)

    # Transform text using the loaded vectorizer
    text_transformed = vectorizer.transform([text])

    # Convert text_transformed to DMatrix
    dtest = xgb.DMatrix(text_transformed)

    # Make predictions using the loaded model
    y_pred = model.predict(dtest)
    return int(y_pred[0])  # Assuming prediction returns a single label

if __name__ == "__main__":
    # Example usage:
    current_dir = Path(__file__).resolve().parent
    file_path = current_dir.parent / 'txtfiles' / 'LegalTest1.txt'

    predicted_label = predict_label_from_file(file_path)
    print("Predicted label:", predicted_label)
