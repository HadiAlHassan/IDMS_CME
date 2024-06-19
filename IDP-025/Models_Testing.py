import joblib
from pathlib import Path

model=joblib.load('logistic_regression_model.pkl')
model2=joblib.load('naive_bayes_model.pkl')
vectorizer=joblib.load('tfidf_vectorizer.pkl')

def classify_text_logistic(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)
    
    return prediction[0]

def classify_text_naive(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model2.predict(text_vector)
    
    return prediction[0]

current_dir=Path(__file__).resolve().parent
text_file_path= current_dir / 'TestCase1.txt'

with open(text_file_path,'r',encoding='utf-8') as file:
    new_text=file.read()

prediction= classify_text_logistic(new_text)
print(f"The predicted label is using logistic regression: {prediction}")

prediction2= classify_text_naive(new_text)
print(f"The predicted label is using naive bayes: {prediction}")
