import joblib
from pathlib import Path

model=joblib.load('logistic_regression_model.pkl')
vectorizer=joblib.load('tfidf_vectorizer.pkl')

def classify_text(text):
    
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)
    
    return prediction[0]

current_dir=Path(__file__).resolve().parent
text_file_path= current_dir / 'TestCase4.txt'

with open(text_file_path,'r',encoding='utf-8') as file:
    new_text=file.read()

prediction= classify_text(new_text)
print(f"The predicted label is: {prediction}")
