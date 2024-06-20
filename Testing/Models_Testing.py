import joblib
from pathlib import Path

model=joblib.load('logistic_regression_model.pkl')
model2=joblib.load('naive_bayes_model.pkl')
model3=joblib.load("RandomForest.pkl")
model4=joblib.load("RandomForest_best_hyperopt.pkl")
model5=joblib.load("LogisticRegression_best_hyperopt.pkl")
model6=joblib.load("naive_bayes_hyperopt.pkl")

vectorizer=joblib.load('tfidf_vectorizer.pkl')

def classify_text_logistic(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)
    
    return prediction[0]

def classify_text_naive(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model2.predict(text_vector)
    
    return prediction[0]

def classify_text_RandomForest(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model3.predict(text_vector)
    
    return prediction[0]

def classify_text_RandomForestHyperopt(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model4.predict(text_vector)
    
    return prediction[0]

def classify_text_LogisticRegressionHyperopt(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model5.predict(text_vector)
    
    return prediction[0]

def classify_text_NaiveBayesHyperopt(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model6.predict(text_vector)
    
    return prediction[0]

current_dir=Path(__file__).resolve().parent
text_file_path= current_dir.parent/ 'TestingTxtFiles' / 'LegalTest1.txt'

with open(text_file_path,'r',encoding='utf-8') as file:
    new_text=file.read()

prediction= classify_text_logistic(new_text)
print(f"The predicted label is using logistic regression: {prediction}")

prediction2= classify_text_naive(new_text)
print(f"The predicted label is using naive bayes: {prediction2}")

prediction3= classify_text_RandomForest(new_text)
print(f"The predicted label is using Random Forest: {prediction3}")

prediction4= classify_text_RandomForestHyperopt(new_text)
print(f"The predicted label is using Random Forest HyperTuned: {prediction4}")

prediction5= classify_text_LogisticRegressionHyperopt(new_text)
print(f"The predicted label is using Logistic Regression HyperTuned: {prediction5}")

prediction6= classify_text_NaiveBayesHyperopt(new_text)
print(f"The predicted label is using Naive Bayes HyperTuned: {prediction6}")
