import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import cross_val_score, train_test_split
from hyperopt import hp, fmin, tpe, Trials
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from nltk.tokenize import word_tokenize

# Define current directory and dataset path
current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Legal_Non_Legal_Dataset.csv'

# Load the dataset
if not dataset_path.exists():
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

dataset = pd.read_csv(dataset_path)

# Load the pre-trained TF-IDF vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Transform the text data

stop_words= set(stopwords.words("english"))

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


X = vectorizer.transform(dataset["clean_text"])
y = dataset["label"]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the search space for hyperparameters
space = {
    'C': hp.loguniform('C', np.log(0.001), np.log(1000)),  # Regularization parameter
    'penalty': hp.choice('penalty', ['l1', 'l2'])  # Penalty type
}

# Define the objective function for hyperparameter optimization
def objective(params):
    model = LogisticRegression(
        C=params['C'],
        penalty=params['penalty'],
        random_state=42,
        solver='liblinear',  # Suitable solver for small datasets
        class_weight='balanced'  # Handle class imbalance
    )
    
    # Evaluate model using cross-validation with F1 score
    cv_score = cross_val_score(model, X_train, y_train, cv=5, scoring='f1_weighted')
    
    return -cv_score.mean()  # Minimize negative F1 score

# Initialize Trials object to keep track of results
trials = Trials()

# Run hyperparameter optimization
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=50,  # Adjust as needed
            trials=trials)

# Print the best hyperparameters
print("Best hyperparameters:")
print(best)

# Extract the best hyperparameters
best_C = best['C']
best_penalty = ['l1', 'l2'][best['penalty']]

print(f"Best C: {best_C}")
print(f"Best penalty: {best_penalty}")

# Instantiate the best model
best_model = LogisticRegression(
    C=best_C,
    penalty=best_penalty,
    random_state=42,
    solver='liblinear',
    class_weight='balanced'
)

# Train the best model on the entire training set
best_model.fit(X_train, y_train)

# Save the best model
joblib.dump(best_model, 'LogisticRegression_best_hyperopt.pkl')

# Evaluate the model on the test set
y_pred = best_model.predict(X_test)

# Calculate the weighted F1 score
f1 = f1_score(y_test, y_pred, average='weighted')
print("Weighted F1 Score:", f1)
print("---------------------")

# Print the classification report
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business', 'Legal']))
print("---------------------")
