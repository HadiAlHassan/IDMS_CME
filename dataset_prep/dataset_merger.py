import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from pathlib import Path

def preprocess_text(text):
    # Remove special characters
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    
    # Tokenize the text
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

def preprocess_text(text):
    # Remove special characters
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    
    # Tokenize the text
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

#Creating the dataset to be used in the word cloud feature
current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'datasets' / 'Court_Case_Cleaned.csv'
dataset_path2 = current_dir.parent / 'datasets' / 'legal_docs_Cleaned.csv'
dataset_path3 = current_dir.parent / 'datasets' / 'MAUD_dev_Cleaned.csv'

ds1 = pd.read_csv(dataset_path)
ds2 = pd.read_csv(dataset_path2)
ds3 = pd.read_csv(dataset_path3)

# Concatenate datasets
df = pd.concat([ds1, ds2, ds3])
df= df.dropna(subset="text")

# Preprocess the "text" column and save it to a new column "clean_text"
df['clean_text'] = df['text'].apply(preprocess_text)

# Drop all other columns except "clean_text"
df_cleaned = df[['clean_text']]

# Save the new DataFrame to a CSV file
output_path = current_dir.parent / 'datasets' / 'legal_merged_dataset.csv'
df_cleaned.to_csv(output_path, index=False)
print(df_cleaned.head())