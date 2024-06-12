import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report


current_dir = Path(__file__).resolve().parent
dataset_path = current_dir / 'Datasets' / 'Language Detection.csv'

# Ensure the file exists
if dataset_path.exists():
    print(f"File found: {dataset_path}")
   
    dataset = pd.read_csv(dataset_path)

    print(dataset.head())
else:
    print(f"File not found: {dataset_path}")


vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3), analyzer='char')
X = vectorizer.fit_transform(dataset['Text']) #feature --> input
y = dataset['Language'] #label --> what we want to predict

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # testing --> 20% of the dataset/ training -->80% / random_state -->Controls the shuffling applied to the data before applying the split.
model = MultinomialNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(classification_report(y_test, y_pred))

file_to_predict=input("Please insert the file name: ")
file_to_predict=file_to_predict + ".txt"
file_path = current_dir / 'TestingTxtFiles' / file_to_predict


if file_path.exists():
    with open(file_path, 'r', encoding='utf-8') as file:
        new_text = file.read()

    
    new_X = vectorizer.transform([new_text])
    prediction = model.predict(new_X)
    print(f"The predicted language is: {prediction[0]}")
else:
    print(f"Test file not found: {file_path}")