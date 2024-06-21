import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,f1_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split, cross_val_score
from hyperopt import hp, fmin, tpe, Trials
import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from nltk.tokenize import word_tokenize

current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Legal_Non_Legal_Dataset.csv'

if not dataset_path.exists():
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

dataset = pd.read_csv(dataset_path)
print(dataset.head())

vectorizer=joblib.load("tfidf_vectorizer.pkl")

lemmatizer = WordNetLemmatizer()
def preprocess_text(text):
    # Convert text to lowercase and remove non-alphanumeric characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize text into words
    words = word_tokenize(text)
    stop_words= set(stopwords.words("english"))
    # Remove stopwords and lemmatize words
    lemmatized_words = []
    for word in words:
        if word not in stop_words:
            lemma = lemmatizer.lemmatize(word)
            lemmatized_words.append(lemma)
    
    return ' '.join(lemmatized_words)

dataset['clean_text'] = dataset['text'].apply(preprocess_text) 

X=vectorizer.fit_transform(dataset["clean_text"])
y=dataset["label"]

X_train,X_test, y_train, y_test= train_test_split(X,y,test_size=0.2,random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred=model.predict(X_test)

print("Weighted F1 score: ", f1_score(y_test, y_pred, average='weighted'))
print("---------------------")
print("Classification report: ")
print(classification_report(y_test,y_pred,target_names=['Politics','Sport','Technology','Entertainment','Business', 'Legal']))
print("---------------------")

#Checking for overfitting 
cross_val_scores = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')
print(f'Cross-Validation F1 Score: {cross_val_scores.mean():.4f} (+/- {cross_val_scores.std():.4f})')
print("---------------------")

model2= joblib.load("RandomForest_best_hyperopt.pkl")

y_pred = model2.predict(X_test)

f1 = f1_score(y_test, y_pred, average='weighted')
print(f"Weighted F1 score on test set: {f1:.4f}")
print("---------------------")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business', "Legal"]))


# Saving the model
joblib.dump(model, 'RandomForest.pkl')