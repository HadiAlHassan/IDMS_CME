import pandas as pd
from wordcloud import WordCloud
import nltk
from nltk.tokenize import word_tokenize
import re
from collections import Counter
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib
import time
 
matplotlib.use('Agg')
 
# Download necessary NLTK data
nltk.download('punkt')
 
def load_stopwords(file_path):
    """Load stopwords from a CSV file line by line and return a set."""
    stopwords_set = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stopword = line.strip()
            if stopword:
                stopwords_set.add(stopword)
    return stopwords_set
 
def preprocess_text(text, stopwords_set):
    """Preprocess text by removing non-alphanumeric characters and stopwords."""
    text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphanumeric characters
    tokens = (word.lower() for word in word_tokenize(text) if word.isalnum())
    tokens = [word for word in tokens if word not in stopwords_set]
    return tokens
 
def read_dataset_in_chunks(file_path, chunk_size=1000):
    """Read dataset in chunks to reduce memory usage."""
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk
 
def generate_word_cloud_from_text(text, stopwords_path, output_path):
    """Generate a word cloud image from a single text string."""
    stopwords_set = load_stopwords(stopwords_path)
    preprocessed_tokens = preprocess_text(text, stopwords_set)
    word_frequencies = Counter(preprocessed_tokens)
 
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        collocations=False,
        max_words=200,
        contour_width=3,
        contour_color='steelblue',
        prefer_horizontal=1.0,
        max_font_size=300,
        min_font_size=20,
        scale=5,
    )
    wordcloud.generate_from_frequencies(word_frequencies)
 
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
    plt.close()
 
def update_dataset_and_generate_word_cloud(input_string, dataset_path, stopwords_path, output_path):
    """Update dataset with a new text string and generate a word cloud image."""
    start_time = time.time()
   
    stopwords_set = load_stopwords(stopwords_path)
   
    # Read dataset in chunks
    dataset_chunks = read_dataset_in_chunks(dataset_path)
   
    # Preprocess new input string
    preprocessed_tokens = preprocess_text(input_string, stopwords_set)
    new_data = pd.DataFrame({'clean_text': [' '.join(preprocessed_tokens)]})
   
    # Update dataset chunk by chunk
    updated_chunks = []
    for chunk in dataset_chunks:
        updated_chunks.append(chunk)
   
    updated_dataset = pd.concat(updated_chunks + [new_data], ignore_index=True)
   
    # Save updated dataset
    updated_dataset.to_csv(dataset_path, index=False)
   
    # Generate word cloud
    word_frequencies = Counter()
    for text in updated_dataset['clean_text'].dropna():
        tokens = preprocess_text(text, stopwords_set)
        word_frequencies.update(tokens)
   
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        collocations=False,
        max_words=200,
        contour_width=3,
        contour_color='steelblue',
        prefer_horizontal=1.0,
        max_font_size=300,
        min_font_size=20,
        scale=5,
    )
    wordcloud.generate_from_frequencies(word_frequencies)
   
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
    plt.close()
 
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")