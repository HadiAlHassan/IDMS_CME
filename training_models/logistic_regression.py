from pathlib import Path
import re
import joblib

from matplotlib import pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, f1_score, confusion_matrix
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Legal_Non_Legal_Dataset.csv'

if not dataset_path.is_file():
    print(f"File not found: {dataset_path}")
else:
    dataset = pd.read_csv(dataset_path)

stop_words= set(stopwords.words("english"))
ps=PorterStemmer()
lemmatizer = WordNetLemmatizer() 
def preprocess_text(text):
    # Convert text to lowercase and remove non-alphanumeric characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize text into words
    words = word_tokenize(text)
    
    # Remove stopwords and lemmatize words
    lemmatized_words = []
    for word in words:
        if word not in stop_words:
            lemma = lemmatizer.lemmatize(word)
            lemmatized_words.append(lemma)
    
    return ' '.join(lemmatized_words)

dataset['clean_text'] = dataset['text'].apply(preprocess_text)    


print(dataset.head())

vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(dataset['clean_text'])
y = dataset['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Logistic Regression Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the Model
y_pred = model.predict(X_test)


cm = confusion_matrix(y_test, y_pred)
cm_display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business', 'Legal'])

print("Confusion Matrix:")
print(cm)

cm_display.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

f1 = f1_score(y_test, y_pred, average='weighted')
print("Weighted F1 Score:", f1)


print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Politics','Sport','Technology','Entertainment','Business','Legal']))

fine_tuned_model=joblib.load("LogisticRegression_best_hyperopt.pkl")
y_pred_fine_tuned=fine_tuned_model.predict(X_test)

print("---------------------")

print(model.classes_) #checking the Labels of the model
print(model.score(X,y))
print("---------------------")

# Evaluate the Normal Logistic Regression Model
f1_normal = f1_score(y_test, y_pred, average='weighted')
print("Normal Logistic Regression - Weighted F1 Score:", f1_normal)
print("Normal Logistic Regression - Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business','Legal']))


# Confusion Matrix for Fine-Tuned Model
cm_fine_tuned = confusion_matrix(y_test, y_pred_fine_tuned)
cm_display_fine_tuned = ConfusionMatrixDisplay(confusion_matrix=cm_fine_tuned, display_labels=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business', 'Legal'])

print("Confusion Matrix for Fine-Tuned Model:")
print(cm_fine_tuned)

cm_display_fine_tuned.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix for Fine-Tuned Model")
plt.show()



# Evaluate the Fine-Tuned Logistic Regression Model
f1_fine_tuned = f1_score(y_test, y_pred_fine_tuned, average='weighted')
print("\nFine-Tuned Logistic Regression - Weighted F1 Score:", f1_fine_tuned)
print("Fine-Tuned Logistic Regression - Classification Report:")
print(classification_report(y_test, y_pred_fine_tuned, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business', 'Legal']))

# Saving the model & Vectorizer
joblib.dump(model, 'logistic_regression_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

