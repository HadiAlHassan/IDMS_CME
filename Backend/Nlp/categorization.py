import joblib
import xgboost as xgb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load the trained model, vectorizer, and label encoder
model_path = BASE_DIR / 'models' / 'XGBoostModel_GPU.joblib'
vectorizer_path = BASE_DIR / 'models' / 'tfidf_vectorizer.joblib'
label_encoder_path = BASE_DIR / 'models' / 'label_encoder.joblib'

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
label_encoder = joblib.load(label_encoder_path)

def predict_label_from_string(text):
    """Predict the label for text data in the given string."""
    # Transform text using the loaded vectorizer
    text_transformed = vectorizer.transform([text])

    # Convert text_transformed to DMatrix
    dtest = xgb.DMatrix(text_transformed)

    # Make predictions using the loaded model
    y_pred = model.predict(dtest)
    
    # Convert numerical label to string label
    predicted_label = label_encoder.inverse_transform([int(y_pred[0])])[0]
    return predicted_label  # Return the string label
