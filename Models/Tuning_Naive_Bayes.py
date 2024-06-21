import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, f1_score
from hyperopt import hp, fmin, tpe, Trials
import joblib
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Define current directory and dataset path
current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Legal_Non_Legal_Dataset.csv'

# Load the dataset
if not dataset_path.is_file():
    raise FileNotFoundError(f"File not found: {dataset_path}")

dataset = pd.read_csv(dataset_path)
print(dataset.head())

# Load the pre-trained TF-IDF vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")
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

# Transform the text data
X = vectorizer.transform(dataset['clean_text'])
y = dataset['label']

# Define the search space for hyperparameters
space = {
    'alpha': hp.uniform('alpha', 0.01, 10)
}

# Define the objective function for hyperparameter optimization
def objective(params):
    model = MultinomialNB(alpha=params['alpha'])
    cv_score = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')
    return -cv_score.mean()  # Minimize negative F1 score

# Initialize Trials object to keep track of results
trials = Trials()

# Run hyperparameter optimization
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=100,  # Adjust as needed
            trials=trials)

# Print the best hyperparameters
print("Best hyperparameters:")
print(best)

# Extract the best alpha
best_alpha = best['alpha']
print(f"Best alpha: {best_alpha}")

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Multinomial Naive Bayes model with the best alpha
model = MultinomialNB(alpha=best_alpha)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
f1 = f1_score(y_test, y_pred, average='weighted')
print("Weighted F1 Score:", f1)
print("---------------------")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Politics','Sport','Technology','Entertainment','Business','Legal']))
print("---------------------")

# Save the trained model and the vectorizer
joblib.dump(model, 'naive_bayes_hyperopt.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
