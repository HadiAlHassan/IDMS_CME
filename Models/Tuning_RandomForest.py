import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from hyperopt import hp, fmin, tpe, Trials
import joblib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the dataset
current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Legal_Non_Legal_dataset.csv'

if not dataset_path.exists():
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

dataset = pd.read_csv(dataset_path)
print(dataset.head())

# # Load the pre-trained vectorizer
# vectorizer = joblib.load("tfidf_vectorizer.pkl")  


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

# # Transform the text data
# X = vectorizer.transform(dataset["clean_text"])
# y = dataset["label"]

# # Split the data into train and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# # Address class imbalance using a combination of SMOTE and RandomUnderSampler
# over_sampler = SMOTE(sampling_strategy='minority', random_state=42)
# under_sampler = RandomUnderSampler(sampling_strategy='majority', random_state=42)
# steps = [('o', over_sampler), ('u', under_sampler)]
# pipeline = Pipeline(steps=steps)

# X_train_resampled, y_train_resampled = pipeline.fit_resample(X_train, y_train)

# # Define the search space for hyperparameter optimization
# space = {
#     'n_estimators': hp.choice('n_estimators', np.arange(50, 500, 50, dtype=int)),  
#     'max_depth': hp.choice('max_depth', np.arange(10, 60, 10, dtype=int)),  
#     'class_weight': hp.choice('class_weight', ['balanced', 'balanced_subsample', None])
# }

# # Define the objective function
# def objective(params):
#     model = RandomForestClassifier(
#         n_estimators=params['n_estimators'],
#         max_depth=params['max_depth'],
#         class_weight=params['class_weight'],
#         random_state=42,
#         n_jobs=-1  # Parallelize the process
#     )
#     cv_score = cross_val_score(model, X_train_resampled, y_train_resampled, cv=3, scoring='f1_weighted', n_jobs=-1)
#     return -cv_score.mean()  # Minimize negative F1 score

# # Run hyperparameter optimization
# trials = Trials()
# best = fmin(fn=objective,
#             space=space,
#             algo=tpe.suggest,
#             max_evals=50,  # Adjust as needed
#             trials=trials)

# # Print the best hyperparameters
# print("Best hyperparameters:")
# print(best)
# best_n_estimators = np.arange(50, 500, 50)[best['n_estimators']]
# best_max_depth = np.arange(10, 60, 10)[best['max_depth']]
# best_class_weight = ['balanced', 'balanced_subsample', None][best['class_weight']]
# print(f"Best n_estimators: {best_n_estimators}")
# print(f"Best max_depth: {best_max_depth}")
# print(f"Best class_weight: {best_class_weight}")

# # Train the best model with the found hyperparameters
# best_model = RandomForestClassifier(
#     n_estimators=best_n_estimators,
#     max_depth=best_max_depth,
#     class_weight={0:0.19, 1:0.19, 2:0.19, 3:0.19, 4:0.19, 5:0.05},
#     random_state=42,
#     n_jobs=-1  # Parallelize the process
# )
# best_model.fit(X_train_resampled, y_train_resampled)

# # Save the best model
# joblib.dump(best_model, 'RandomForest_best_hyperopt.pkl')

# # Evaluate the best model on the test set
# y_pred_best = best_model.predict(X_test)
# f1_best = f1_score(y_test, y_pred_best, average='weighted')
# print(f"Weighted F1 score on test set: {f1_best:.4f}")
# print("---------------------")
# print("Classification Report:")
# print(classification_report(y_test, y_pred_best, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business', 'Legal']))

# # Cross-validation score for checking overfitting
# cv_score = cross_val_score(best_model, X_train_resampled, y_train_resampled, cv=3, scoring='f1_weighted', n_jobs=-1)
# print(f'Cross-Validation F1 Score: {cv_score.mean():.4f} (+/- {cv_score.std():.4f})')
# print("---------------------")


##############trying#####

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

X = dataset['clean_text']
y = dataset['label']

tfidf = TfidfVectorizer(max_features=10000)
X_tfidf = tfidf.fit_transform(X)

# First, split off the test set (20% of the data)
X_temp, X_test, y_temp, y_test = train_test_split(X_tfidf, y, test_size=0.2, stratify=y, random_state=42)

# Then, split the remaining data into training and validation sets (60% training, 20% validation)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, stratify=y_temp, random_state=42)

class_weights = {
    0: 0.19,
    1: 0.19,
    2: 0.19,
    3: 0.19,
    4: 0.19,
    5: 0.05
}

# Define the search space
search_space = {
    'n_estimators': hp.choice('n_estimators', [100, 200, 300]),
    'max_depth': hp.choice('max_depth', [10, 20, 30]),
    'criterion': hp.choice('criterion', ['gini', 'entropy'])
}

# Define the objective function
def objective(params):
    model = RandomForestClassifier(
        n_estimators=params['n_estimators'],
        max_depth=params['max_depth'],
        criterion=params['criterion'],
        class_weight=class_weights,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    y_val_pred = model.predict(X_val)
    f1 = f1_score(y_val, y_val_pred, average='macro')
    
    return {'loss': -f1, 'status': STATUS_OK}

# Initialize the trials object
trials = Trials()

# Use default_rng for the random state
rng = np.random.default_rng(42)

# Run the optimization
best_params = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=50,
    trials=trials,
    rstate=rng
)

print("Best parameters:", best_params)

# Translate the best parameters back to their values
best_n_estimators = [100, 200, 300][best_params['n_estimators']]
best_max_depth = [10, 20, 30][best_params['max_depth']]
best_criterion = ['gini', 'entropy'][best_params['criterion']]

print(f"Best n_estimators: {best_n_estimators}")
print(f"Best max_depth: {best_max_depth}")
print(f"Best criterion: {best_criterion}")

# Initialize the RandomForestClassifier with the best parameters
best_model = RandomForestClassifier(
    n_estimators=best_n_estimators,
    max_depth=best_max_depth,
    criterion=best_criterion,
    class_weight=class_weights,
    random_state=42,
    n_jobs=-1
)

# Train the model
best_model.fit(X_train, y_train)

# Make predictions on the validation set
y_val_pred = best_model.predict(X_val)

# Evaluate the model on the validation set
from sklearn.metrics import classification_report
print("Validation Set Classification Report:")
print(classification_report(y_val, y_val_pred))

# Make predictions on the test set
y_test_pred = best_model.predict(X_test)

# Evaluate the model on the test set
print("Test Set Classification Report:")
print(classification_report(y_test, y_test_pred))