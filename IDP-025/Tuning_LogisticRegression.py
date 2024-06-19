import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
from hyperopt import hp, fmin, tpe, Trials
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Non_legal_dataset.csv'

if not dataset_path.exists():
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

dataset = pd.read_csv(dataset_path)
vectorizer = joblib.load("tfidf_vectorizer.pkl")

X = vectorizer.transform(dataset["Text"])
y = dataset["Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

space = {
    'C': hp.loguniform('C', np.log(0.001), np.log(1000)),  # Regularization parameter
    'penalty': hp.choice('penalty', ['l1', 'l2'])  # Penalty type
}

# Define objective function
def objective(params):
    # Instantiate the model with current hyperparameters
    model = LogisticRegression(
        C=params['C'],
        penalty=params['penalty'],
        random_state=42,
        solver='liblinear'  # Suitable solver for small datasets
    )
    
    # Evaluate model using cross-validation with F1 score
    cv_score = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')
    
    # Return the negative F1 score (to minimize)
    return -cv_score.mean()

# Initialize Trials object to keep track of results
trials = Trials()

# Run optimization
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=50,  # Adjust as needed
            trials=trials)

# Print best hyperparameters found
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
    solver='liblinear'
)

# Train the model on the entire dataset
best_model.fit(X, y)

# Save the best model
joblib.dump(best_model, 'LogisticRegression_best_hyperopt.pkl')