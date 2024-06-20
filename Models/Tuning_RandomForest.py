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

# Load the dataset
current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Legal_Non_Legal_dataset.csv'

if not dataset_path.exists():
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

dataset = pd.read_csv(dataset_path)
print(dataset.head())

# Load the pre-trained vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")  

# Transform the text data
X = vectorizer.transform(dataset["text"])
y = dataset["label"]

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Address class imbalance using a combination of SMOTE and RandomUnderSampler
over_sampler = SMOTE(sampling_strategy='minority', random_state=42)
under_sampler = RandomUnderSampler(sampling_strategy='majority', random_state=42)
steps = [('o', over_sampler), ('u', under_sampler)]
pipeline = Pipeline(steps=steps)

X_train_resampled, y_train_resampled = pipeline.fit_resample(X_train, y_train)

# Define the search space for hyperparameter optimization
space = {
    'n_estimators': hp.choice('n_estimators', np.arange(50, 500, 50, dtype=int)),  # Reduced range
    'max_depth': hp.choice('max_depth', np.arange(10, 60, 10, dtype=int)),  # Reduced range
    'class_weight': hp.choice('class_weight', ['balanced', 'balanced_subsample', None])
}

# Define the objective function
def objective(params):
    model = RandomForestClassifier(
        n_estimators=params['n_estimators'],
        max_depth=params['max_depth'],
        class_weight=params['class_weight'],
        random_state=42,
        n_jobs=-1  # Parallelize the process
    )
    cv_score = cross_val_score(model, X_train_resampled, y_train_resampled, cv=3, scoring='f1_weighted', n_jobs=-1)
    return -cv_score.mean()  # Minimize negative F1 score

# Run hyperparameter optimization
trials = Trials()
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=50,  # Adjust as needed
            trials=trials)

# Print the best hyperparameters
print("Best hyperparameters:")
print(best)
best_n_estimators = np.arange(50, 500, 50)[best['n_estimators']]
best_max_depth = np.arange(10, 60, 10)[best['max_depth']]
best_class_weight = ['balanced', 'balanced_subsample', None][best['class_weight']]
print(f"Best n_estimators: {best_n_estimators}")
print(f"Best max_depth: {best_max_depth}")
print(f"Best class_weight: {best_class_weight}")

# Train the best model with the found hyperparameters
best_model = RandomForestClassifier(
    n_estimators=best_n_estimators,
    max_depth=best_max_depth,
    class_weight=best_class_weight,
    random_state=42,
    n_jobs=-1  # Parallelize the process
)
best_model.fit(X_train_resampled, y_train_resampled)

# Save the best model
joblib.dump(best_model, 'RandomForest_best_hyperopt.pkl')

# Evaluate the best model on the test set
y_pred_best = best_model.predict(X_test)
f1_best = f1_score(y_test, y_pred_best, average='weighted')
print(f"Weighted F1 score on test set: {f1_best:.4f}")
print("---------------------")
print("Classification Report:")
print(classification_report(y_test, y_pred_best, target_names=['Politics', 'Sport', 'Technology', 'Entertainment', 'Business', 'Legal']))

# Cross-validation score for checking overfitting
cv_score = cross_val_score(best_model, X_train_resampled, y_train_resampled, cv=3, scoring='f1_weighted', n_jobs=-1)
print(f'Cross-Validation F1 Score: {cv_score.mean():.4f} (+/- {cv_score.std():.4f})')
print("---------------------")
