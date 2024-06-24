from pathlib import Path
import joblib

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score, classification_report


current_dir= Path(__file__).resolve().parent
dataset_path= current_dir.parent / 'Datasets'/ 'Legal_Non_Legal_Dataset.csv'

if not dataset_path.is_file():
    print(f"File not found: {dataset_path}")
else:
    dataset = pd.read_csv(dataset_path)

# Assuming tfidf_vectorizer.pkl is in the correct directory
vectorizer_path = Path(__file__).resolve().parent.parent / 'models' / 'tfidf_vectorizer.pkl'

# Load the TF-IDF vectorizer
vectorizer = joblib.load(vectorizer_path)

X=vectorizer.fit_transform(dataset["text"]) #feature
y=dataset["label"]

X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.2, random_state=42)


model= MultinomialNB() #Training the Model
model.fit(X_train,y_train)

y_pred= model.predict(X_test) #predicting

print("Weighted F1 score: ", f1_score(y_test, y_pred, average='weighted'))
print("---------------------")
print("Classification report: ")
print(classification_report(y_test,y_pred,target_names=['Politics','Sport','Technology','Entertainment','Business', 'Legal']))

#Saving the model
joblib.dump(model, 'naive_bayes_model.pkl')