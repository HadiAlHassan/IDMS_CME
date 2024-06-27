import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import xgboost as xgb
import numpy as np

# Load the data from CSV
data = pd.read_csv('NLP_Dataset_Cleaned_With_Category.csv')
print(data.head())

data = data.dropna(subset=["clean_text"])
X = data['clean_text']
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to TF-IDF features
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Initialize LabelEncoder
label_encoder = LabelEncoder()

# Fit label encoder and transform labels
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Convert data to DMatrix format
dtrain = xgb.DMatrix(X_train_tfidf, label=y_train_encoded)
dtest = xgb.DMatrix(X_test_tfidf, label=y_test_encoded)

params = {
    'objective': 'multi:softmax',
    'num_class': len(np.unique(y_train)),
    'eval_metric': 'merror',
    'tree_method': 'gpu_hist',
    'predictor': 'gpu_predictor',
    'device': 'gpu'
}

# Train the XGBoost model
num_rounds = 100
model = xgb.train(params, dtrain, num_rounds)

# Make predictions on the test set
y_pred = model.predict(dtest)

# Inverse transform the predicted labels
y_pred_decoded = label_encoder.inverse_transform(y_pred.astype(int))

# Print the classification report
print(classification_report(y_test, y_pred_decoded))

# Save the trained model and the vectorizer
joblib.dump(model, 'XGBoostModel_GPU.joblib')
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')
joblib.dump(label_encoder, 'label_encoder.joblib')
print("Model, vectorizer, and label encoder saved.")

# Access the original classes
original_classes = label_encoder.classes_

# Map predicted labels to their corresponding class names
predicted_labels_with_classes = [original_classes[label] for label in y_pred.astype(int)]

# Print predicted labels with their corresponding class names
for label, class_name in zip(y_pred.astype(int), predicted_labels_with_classes):
    print(f"Predicted label {label} corresponds to class '{class_name}'")
