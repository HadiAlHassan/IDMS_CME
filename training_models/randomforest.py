from pathlib import Path
import re
import joblib

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split, cross_val_score
from scipy.stats import randint
from sklearn.tree import export_graphviz
from IPython.display import Image
#import graphviz
from sklearn.multioutput import MultiOutputClassifier
from hyperopt import hp, fmin, tpe, Trials
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'datasets' / 'NLP_Dataset_Cleaned_With_Category.csv'

random_state=42

if not dataset_path.exists():
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

dataset = pd.read_csv(dataset_path)
print(dataset.head())


# # Assuming tfidf_vectorizer.pkl is in the correct directory
# vectorizer_path = Path(__file__).resolve().parent.parent / 'models' / 'tfidf_vectorizer.pkl'

# # Load the TF-IDF vectorizer
# vectorizer = joblib.load(vectorizer_path)

# lemmatizer = WordNetLemmatizer()
# def preprocess_text(text):
#     # Convert text to lowercase and remove non-alphanumeric characters
#     text = text.lower()
#     text = re.sub(r'[^\w\s]', '', text)
    
#     # Tokenize text into words
#     words = word_tokenize(text)
#     stop_words= set(stopwords.words("english"))
#     # Remove stopwords and lemmatize words
#     lemmatized_words = []
#     for word in words:
#         if word not in stop_words:
#             lemma = lemmatizer.lemmatize(word)
#             lemmatized_words.append(lemma)
    
#     return ' '.join(lemmatized_words)

# dataset['clean_text'] = dataset['text'].apply(preprocess_text) 

# X=vectorizer.fit_transform(dataset["clean_text"])
# y=dataset["label"]

# X_train,X_test, y_train, y_test= train_test_split(X,y,test_size=0.2,random_state=42)

# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# y_pred=model.predict(X_test)

# print("Weighted F1 score: ", f1_score(y_test, y_pred, average='weighted'))
# print("---------------------")
# print("Classification report: ")
# print(classification_report(y_test,y_pred,target_names=['Politics','Sport','Technology','Entertainment','Business', 'Legal']))
# print("---------------------")

# #Checking for overfitting 
# cross_val_scores = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')
# print(f'Cross-Validation F1 Score: {cross_val_scores.mean():.4f} (+/- {cross_val_scores.std():.4f})')
# print("---------------------")

# model2= joblib.load("RandomForest_best_hyperopt.pkl")

# y_pred = model2.predict(X_test)

# f1 = f1_score(y_test, y_pred, average='weighted')
# print(f"Weighted F1 score on test set: {f1:.4f}")
# print("---------------------")
# print("Classification Report:")
# print(classification_report(y_test, y_pred, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business', "Legal"]))


# # Saving the model
# joblib.dump(model, 'RandomForest.pkl')

##############

#Splitting the data into features (X) & Target (y)
dataset['clean_text'].fillna("", inplace=True)

X = dataset['clean_text']
y=dataset[["label", "category"]]

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust max_features as needed

# Fit and transform the text data
X_transformed = vectorizer.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_transformed, y, test_size=0.2, random_state=42
)


rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42, verbose=1)

# Initialize MultiOutputClassifier
multi_target_rf = MultiOutputClassifier(rf_classifier, n_jobs=-1)  # n_jobs=-1 for parallel processing

# Train the model
multi_target_rf.fit(X_train, y_train)

# Predict labels and categories
y_pred = multi_target_rf.predict(X_test)

# Calculate accuracy for each target
accuracy_label = accuracy_score(y_test['label'], y_pred[:, 0])
accuracy_category = accuracy_score(y_test['category'], y_pred[:, 1])

print(f'Label Accuracy: {accuracy_label}')
print(f'Category Accuracy: {accuracy_category}')

joblib.dump(multi_target_rf, 'multi_output_random_forest.joblib')

print("Multi-output RandomForest model saved successfully.")
