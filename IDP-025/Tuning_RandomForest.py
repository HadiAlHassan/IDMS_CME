import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
from hyperopt import hp, fmin, tpe, Trials
import joblib
from pathlib import Path


current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Non_legal_dataset.csv'

if not dataset_path.exists():
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

dataset = pd.read_csv(dataset_path)
print(dataset.head())

vectorizer = joblib.load("tfidf_vectorizer.pkl")  

X = vectorizer.fit_transform(dataset["Text"])
y = dataset["Label"]


space = {
    'n_estimators': hp.choice('n_estimators', np.arange(50, 1000, 50, dtype=int)),
    'max_depth': hp.choice('max_depth', np.arange(10, 110, 10, dtype=int))
}


def objective(params):

    model = RandomForestClassifier(
        n_estimators=params['n_estimators'],
        max_depth=params['max_depth'],
        random_state=42
    )
    
    # Evaluate model using cross-validation with F1 score
    cv_score = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')
    
    
    return -cv_score.mean()  # Minimize negative F1 score

trials = Trials()

best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=10,  # adjust as needed
            trials=trials)

# Print best hyperparameters found
print("Best hyperparameters:")
print(best)

# Extract the best hyperparameters
best_n_estimators = np.arange(50, 1000, 50)[best['n_estimators']]
best_max_depth = np.arange(10, 110, 10)[best['max_depth']]

print(f"Best n_estimators: {best_n_estimators}")
print(f"Best max_depth: {best_max_depth}")


best_model = RandomForestClassifier(
    n_estimators=best_n_estimators,
    max_depth=best_max_depth,
    random_state=42
)

best_model.fit(X, y)

joblib.dump(best_model, 'RandomForest_best_hyperopt.pkl')
