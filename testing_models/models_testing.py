import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

# Define paths to models
models_dir = Path(__file__).resolve().parent.parent / 'models'

# Load all models and vectorizer
model_logistic = joblib.load(models_dir / 'logistic_regression_model.pkl')
model_naive_bayes = joblib.load(models_dir / 'naive_bayes_model.pkl')
model_rf = joblib.load(models_dir / 'RandomForest.pkl')
model_rf_hyperopt = joblib.load(models_dir / 'RandomForest_best_hyperopt.pkl')
model_lr_hyperopt = joblib.load(models_dir / 'LogisticRegression_best_hyperopt.pkl')
model_nb_hyperopt = joblib.load(models_dir / 'naive_bayes_hyperopt.pkl')
vectorizer = joblib.load(models_dir / 'tfidf_vectorizer.pkl')

def classify_text(text, model):
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)
    return prediction[0]

# Define file path for testing
current_dir = Path(__file__).resolve().parent
text_file_path = current_dir.parent / 'TestingTxtFiles' / 'TestCase5.txt'

with open(text_file_path, 'r', encoding='utf-8') as file:
    new_text = file.read()

# Classify using each model
predictions = {
    'Logistic Regression': classify_text(new_text, model_logistic),
    'Naive Bayes': classify_text(new_text, model_naive_bayes),
    'Random Forest': classify_text(new_text, model_rf),
    'Random Forest HyperTuned': classify_text(new_text, model_rf_hyperopt),
    'Logistic Regression HyperTuned': classify_text(new_text, model_lr_hyperopt),
    'Naive Bayes HyperTuned': classify_text(new_text, model_nb_hyperopt)
}

# Print predictions
for model_name, prediction in predictions.items():
    print(f"The predicted label using {model_name}: {prediction}")
