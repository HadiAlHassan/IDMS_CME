# import pandas as pd
# from wordcloud import WordCloud
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# import re
# from collections import Counter
# import matplotlib.pyplot as plt

# # Download necessary NLTK data
# nltk.download('punkt')

# def load_stopwords(file_path):
#     df = pd.read_csv(file_path)
#     stopwords_list = df[df.columns[0]].tolist()
#     return set(stopwords_list)

# def preprocess_text(text, stopwords_set):
#     text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphanumeric characters
#     tokens = word_tokenize(text)
#     tokens = [word.lower() for word in tokens]
#     tokens = [word for word in tokens if word.isalnum() and word not in stopwords_set]
#     return tokens

# def generate_word_cloud_from_text(text, stopwords_set, output_path):
#     preprocessed_tokens = preprocess_text(text, stopwords_set)
#     word_frequencies = Counter(preprocessed_tokens)
    
#     wordcloud = WordCloud(
#         width=1600,
#         height=800,
#         background_color='white',
#         collocations=False,
#         max_words=200,
#         contour_width=3,
#         contour_color='steelblue',
#         prefer_horizontal=1.0,
#         max_font_size=300,
#         min_font_size=20,
#         scale=5,
#     )
#     wordcloud.generate_from_frequencies(word_frequencies)
    
#     plt.figure(figsize=(16, 8))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
#     plt.close()
    
# def update_dataset_and_generate_word_cloud(input_string, dataset_path, stopwords_set, output_path):
#     # Read the existing dataset
#     dataset = pd.read_csv(dataset_path)
    
#     # Preprocess and add the new string to the dataset
#     preprocessed_tokens = preprocess_text(input_string, stopwords_set)
#     new_row = pd.DataFrame({'clean_text': [' '.join(preprocessed_tokens)]})
#     dataset = pd.concat([dataset, new_row], ignore_index=True)
    
#     # Save the updated DataFrame to the CSV file
#     dataset.to_csv(dataset_path, index=False)
    
#     # Compute word frequencies from the updated dataset
#     word_frequencies = Counter()
#     for text in dataset['clean_text'].dropna():
#         tokens = preprocess_text(text, stopwords_set)
#         word_frequencies.update(tokens)
    
#     # Generate and save the word cloud image
#     wordcloud = WordCloud(
#         width=1600,
#         height=800,
#         background_color='white',
#         collocations=False,
#         max_words=200,
#         contour_width=3,
#         contour_color='steelblue',
#         prefer_horizontal=1.0,
#         max_font_size=300,
#         min_font_size=20,
#         scale=5,
#     )
#     wordcloud.generate_from_frequencies(word_frequencies)
    
#     plt.figure(figsize=(16, 8))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
#     plt.close()

# # File paths
# stopwords_path = 'Datasets/stopwords_english.csv'
# dataset_path = 'Datasets/legal_merged_dataset.csv'
# input_string = """
# As the Celtics players and coaches spent the week celebrating leading up to the parade, Brad Stevens was back at the Auerbach Center, working out dozens of prospects they could select in the draft this week. They have the 30th and 54th picks and are over the second apron, so they have to nail it on draft night to help build a sustainable team over the coming years.

# That’s why after an evening of popping champagne bottles, the front office was back in the early afternoon to get ready for the future.

# “The day after, as much as we were excited and celebratory and everything else, you’re always thinking about what this means for what’s next,” Stevens said. “I think that’s just maybe the coach in me or maybe that’s just my age.”

# Stevens made a stir last year when the Celtics traded down multiple times on draft night to accumulate a bevy of future second-round picks while selecting Jordan Walsh with the 38th pick. That is not necessarily going to be the norm for this franchise, particularly since bigger deals for Payton Pritchard and potentially Sam Hauser mean the Celtics need to draft more players who have a chance at making the rotation while they are still on their rookie-scale contracts.

# Their long-term depth at center is dubious, considering Al Horford’s age and Kristaps Porziņģis’ forthcoming ankle surgery, expected to happen in the next few weeks.

# “Kristaps is still in the middle of consulting with some different doctors and specialists, but we anticipate surgery will be soon,” he said.

# Because the second apron takes away most of their roster-building tools beyond signing free agents to minimum contracts, getting a center who can develop into a starter down the road most likely would come through the draft. Xavier Tillman and Luke Kornet are both free agents, while Neemias Queta is still under contract, but those players are all far along in their development track.

# That’s why Stevens said they made so many trades last season, since they no longer can aggregate salaries in a trade.

# “It’ll be interesting to see how it affects the league,” Stevens said. “Are there a lot less trades? That will be interesting to follow and look back and study over the next couple of years. As far as the picks go, if the right person is available at 30, we will take him.”
# """

# # Paths for word cloud images
# output_path_string = 'wordcloud_from_string.png'
# output_path_dataset = 'wordcloud_from_dataset.png'

# # Load stopwords
# stopwords_set = load_stopwords(stopwords_path)

# # Generate word cloud from the input string
# generate_word_cloud_from_text(input_string, stopwords_set, output_path_string)

# # Update dataset and generate word cloud from the dataset
# update_dataset_and_generate_word_cloud(input_string, dataset_path, stopwords_set, output_path_dataset)

########TRYING4#########
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

def generate_word_cloud_from_text(text, stopwords_set, output_path):
    """Generate a word cloud image from a single text string."""
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
