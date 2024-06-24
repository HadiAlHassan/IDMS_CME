import re
import string
import warnings
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import trange
from wordcloud import WordCloud


current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'datasets' / 'NLP_Dataset_Cleaned_With_Category.csv'


if not dataset_path.is_file():
    print(f"File not found: {dataset_path}")
else:
    
    dataset = pd.read_csv(dataset_path)


#Initial Inspection: Data structure, types, basic info
print(dataset.head())
print("-------------")
print(dataset.info())
print("-------------")
print(dataset["label"].value_counts())
print("-------------")

#Shape
print("Shape of data: ", dataset.shape) # --> (2225 rows, 2 column)
print("-------------")

#Data Cleaning & Handling missing values
dataset=dataset.drop_duplicates()
dataset=dataset.dropna()
print(dataset.isnull().sum())
print("-------------")

# Basic statistics of the text length
dataset['text_length'] = dataset['text'].apply(lambda x: len(x.split()))
print(dataset['text_length'].describe())
print("-------------")

dataset=dataset.groupby('label').filter(lambda x:len(x)>200).reset_index(drop=True)
print('Label=>',len(dataset['label'].unique())) # Checking the number of labels that has a minimum of 200 texts
print("-------------")

stop_words= set(stopwords.words("english"))
ps=PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Convert text to lowercase and remove non-alphanumeric characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize text into words
    words = word_tokenize(text)
    
    # Remove stopwords and lemmatize words
    lemmatized_words = []
    for word in words:
        if word not in stop_words:
            lemma = lemmatizer.lemmatize(word)
            lemmatized_words.append(lemma)
    
    return ' '.join(lemmatized_words)

dataset['clean_text'] = dataset['text'].apply(preprocess_text)
print(dataset['clean_text'].head())
print("-------------")


# Plotting the number of labels per text // label distribution
label_counts = dataset['label'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
label_counts.plot(kind='bar', color='red')
plt.title('Number of Texts per Label')
plt.xlabel('Label')
plt.ylabel('Number of Texts')
plt.xticks(rotation=0)
plt.show()

#Most Common words in the dataset
all_text = ' '.join(dataset['clean_text'])
word_counts = Counter(all_text.split())
common_words = word_counts.most_common(20)
print(common_words)
print("-------------")

# Word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(dataset['clean_text']))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud')
plt.show()

#N-gram

def plot_ngrams(texts,n,top_k):
    vec=CountVectorizer(ngram_range=(n,n))
    ngrams = vec.fit_transform(texts)
    ngrams = vec.fit_transform(texts)
    sum_ngrams = ngrams.sum(axis=0)
    ngram_freq = [(word, sum_ngrams[0, idx]) for word, idx in vec.vocabulary_.items()]
    ngram_freq = sorted(ngram_freq, key=lambda x: x[1], reverse=True)[:top_k]
    
    df_ngram = pd.DataFrame(ngram_freq, columns=['ngram', 'frequency'])
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='frequency', y='ngram', data=df_ngram)
    plt.title(f'Top {top_k} {n}-grams')
    plt.xlabel('Frequency')
    plt.ylabel(f'{n}-gram')
    plt.show()
   
#Testing some n-grams plots
plot_ngrams(dataset['clean_text'], n=2, top_k=20)
plot_ngrams(dataset['clean_text'], n=3, top_k=20)


