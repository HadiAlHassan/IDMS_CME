import pandas as pd
from wordcloud import WordCloud
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from collections import Counter
import matplotlib.pyplot as plt

# Download necessary NLTK data
nltk.download('punkt')

def load_stopwords(file_path):
    """Load stopwords from a CSV file."""
    df = pd.read_csv(file_path)
    stopwords_list = df[df.columns[0]].tolist()
    return set(stopwords_list)

def preprocess_text(text, stopwords_set):
    
    """Preprocess text by removing non-alphanumeric characters and stopwords."""
    text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphanumeric characters
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords_set]
    return tokens

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
    plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
    plt.close()
    
def update_dataset_and_generate_word_cloud(input_string, dataset_path, stopwords_set, output_path):
    """Update dataset with a new text string and generate a word cloud image."""
    # Read the existing dataset
    dataset = pd.read_csv(dataset_path)
    
    # Preprocess and add the new string to the dataset
    preprocessed_tokens = preprocess_text(input_string, stopwords_set)
    new_row = pd.DataFrame({'clean_text': [' '.join(preprocessed_tokens)]})
    dataset = pd.concat([dataset, new_row], ignore_index=True)
    
    # Save the updated DataFrame to the CSV file
    dataset.to_csv(dataset_path, index=False)
    
    # Compute word frequencies from the updated dataset
    word_frequencies = Counter()
    for text in dataset['clean_text'].dropna():
        tokens = preprocess_text(text, stopwords_set)
        word_frequencies.update(tokens)
    
    # Generate and save the word cloud image
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
    plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
    plt.close()
