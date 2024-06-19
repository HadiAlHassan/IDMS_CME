import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,f1_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.model_selection import GridSearchCV
import joblib

current_dir=Path(__file__).resolve().parent
dataset_path= current_dir.parent/'IDP-024' /'Non_legal_dataset.csv'

dataset= pd.read_csv(dataset_path)

print(dataset.head())

vectorizer=joblib.load("tfidf_vectorizer.pkl")

X=vectorizer.fit_transform(dataset["Text"])
y=dataset["Label"]

X_train,X_test, y_train, y_test= train_test_split(X,y,test_size=0.2,random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred=model.predict(X_test)

print("Weighted F1 score: ", f1_score(y_test, y_pred, average='weighted'))
print("---------------------")
print("Classification report: ")
print(classification_report(y_test,y_pred,target_names=['Politics','Sport','Technology','Entertainment','Business']))
print("---------------------")

# defining parameter range 
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2']
}

# Instantiate GridSearchCV
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1)

# Fit GridSearchCV
grid_search.fit(X, y)

# Print the best parameters found
print("Best parameters found:")
print(grid_search.best_params_)

#Saving the model
joblib.dump(model, 'RandomForest.pkl')