import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score, classification_report
import joblib

current_dir= Path(__file__).resolve().parent
dataset_path= current_dir.parent / 'IDP-024'/ 'Non_legal_dataset.csv'

if not dataset_path.is_file():
    print(f"File not found: {dataset_path}")
else:
    dataset = pd.read_csv(dataset_path)

vectorizer= joblib.load('tfidf_vectorizer.pkl')
X=vectorizer.fit_transform(dataset["Text"]) #feature
y=dataset["Label"]

X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.2, random_state=42)


model= MultinomialNB() #Training the Model
model.fit(X_train,y_train)

y_pred= model.predict(X_test) #predicting

print("Weighted F1 score: ", f1_score(y_test, y_pred, average='weighted'))
print("---------------------")
print("Classification report: ")
print(classification_report(y_test,y_pred,target_names=['Politics','Sport','Technology','Entertainment','Business']))

#Saving the model
joblib.dump(model, 'naive_bayes_model.pkl')