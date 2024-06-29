import matplotlib
matplotlib.use('Agg')
import re
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from io import BytesIO
from pathlib import Path
from collections import Counter
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt') 
nltk.download('stopwords') 
nltk.download('wordnet')
def preprocess_text(text):
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]

    # Remove all stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def update_word_frequencies(word_frequencies, new_words):
    for word in new_words:
        word_frequencies[word] += 1

def generate_word_cloud_from_string(input_string, csv_path, output_path):
    # Preprocess the input string
    preprocessed_tokens = preprocess_text(input_string)
    
    # Read the existing dataset
    dataset = pd.read_csv(csv_path)
    
    # Append the preprocessed string to the 'clean_text' column
    new_row = pd.DataFrame({'clean_text': [' '.join(preprocessed_tokens)]})
    dataset = pd.concat([dataset, new_row], ignore_index=True)
    
    # Save the updated DataFrame to the CSV file
    dataset.to_csv(csv_path, index=False)
    
    # Compute word frequencies from the dataset
    word_frequencies = Counter()
    for text in dataset['clean_text'].dropna():
        word_frequencies.update(text.split())
    
    # Update word frequencies with the new input string
    update_word_frequencies(word_frequencies, preprocessed_tokens)
    
    # Generate the word cloud using the updated word frequencies
    wordcloud = WordCloud(width=800, height=400, background_color='white')
    wordcloud.generate_from_frequencies(word_frequencies)
    # Plot the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save the plot to a BytesIO object as SVG
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='svg')
    plt.close()
    
    # Get the SVG data from the buffer
    img_buffer.seek(0)
    svg_data = img_buffer.getvalue().decode('utf-8')
    
    # Save the SVG data to a file
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write(svg_data)
    
    return output_path