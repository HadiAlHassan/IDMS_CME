from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from io import BytesIO
import re

def preprocess_text(text):
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)

    tokens = word_tokenize(text)

    # Convert the tokens to lower case
    tokens = [word.lower() for word in tokens]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join tokens to form the preprocessed text
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

def generate_word_cloud_from_file(file):
    text = file.read()

    preprocessed_text = preprocess_text(text)
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(preprocessed_text)

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
    output_path = 'wordcloud.svg'
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write(svg_data)

    return output_path

# Testing the function
if __name__ == "__main__":
    from pathlib import Path

    
    file_path = Path(__file__).resolve().parent.parent / 'txtfiles' / 'testcase0.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        output_path = generate_word_cloud_from_file(file)
        print(f"Word cloud saved to {output_path}")
