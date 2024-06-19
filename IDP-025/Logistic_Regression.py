import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
import joblib

current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Non_legal_dataset.csv'

if not dataset_path.is_file():
    print(f"File not found: {dataset_path}")
else:
    dataset = pd.read_csv(dataset_path)

print(dataset.head())

vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(dataset['Text'])
y = dataset['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Logistic Regression Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the Model
y_pred = model.predict(X_test)


f1 = f1_score(y_test, y_pred, average='weighted')
print("Weighted F1 Score:", f1)


print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Politics','Sport','Technology','Entertainment','Business']))

fine_tuned_model=joblib.load("LogisticRegression_best_hyperopt.pkl")
y_pred_fine_tuned=fine_tuned_model.predict(X_test)

print("---------------------")

# Evaluate the Normal Logistic Regression Model
f1_normal = f1_score(y_test, y_pred, average='weighted')
print("Normal Logistic Regression - Weighted F1 Score:", f1_normal)
print("Normal Logistic Regression - Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business']))

# Evaluate the Fine-Tuned Logistic Regression Model
f1_fine_tuned = f1_score(y_test, y_pred_fine_tuned, average='weighted')
print("\nFine-Tuned Logistic Regression - Weighted F1 Score:", f1_fine_tuned)
print("Fine-Tuned Logistic Regression - Classification Report:")
print(classification_report(y_test, y_pred_fine_tuned, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business']))

# Saving the model & Vectorizer
# joblib.dump(model, 'logistic_regression_model.pkl')
# joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

