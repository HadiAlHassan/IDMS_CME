# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# import re
# import pandas as pd
# from io import BytesIO
# from pathlib import Path
# from collections import Counter

# def preprocess_text(text):
#     text = re.sub(r'[^A-Za-z0-9\s]', '', text)
#     tokens = word_tokenize(text)
#     tokens = [word.lower() for word in tokens]

#     # Remove all stop words
#     stop_words = set(stopwords.words('english'))
#     tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(word) for word in tokens]
#     return tokens

# def update_word_frequencies(word_frequencies, new_words):
#     for word in new_words:
#         word_frequencies[word] += 1

# def generate_word_cloud_from_string(input_string, csv_path, output_path):
#     # Preprocess the input string
#     preprocessed_tokens = preprocess_text(input_string)
    
#     # Read the existing dataset
#     dataset = pd.read_csv(csv_path)
    
#     # Append the preprocessed string to the 'clean_text' column
#     new_row = pd.DataFrame({'clean_text': [' '.join(preprocessed_tokens)]})
#     dataset = pd.concat([dataset, new_row], ignore_index=True)
    
#     # Save the updated DataFrame to the CSV file
#     dataset.to_csv(csv_path, index=False)
    
#     # Compute word frequencies from the dataset
#     word_frequencies = Counter()
#     for text in dataset['clean_text'].dropna():
#         word_frequencies.update(text.split())
    
#     # Update word frequencies with the new input string
#     update_word_frequencies(word_frequencies, preprocessed_tokens)
    
#     # Generate the word cloud using the updated word frequencies
#     wordcloud = WordCloud(width=800, height=400, background_color='white')
#     wordcloud.generate_from_frequencies(word_frequencies)
    
#     # Plot the word cloud
#     plt.figure(figsize=(10, 5))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis('off')
    
#     # Save the plot to a BytesIO object as SVG
#     img_buffer = BytesIO()
#     plt.savefig(img_buffer, format='svg')
#     plt.close()
    
#     # Get the SVG data from the buffer
#     img_buffer.seek(0)
#     svg_data = img_buffer.getvalue().decode('utf-8')
    
#     # Save the SVG data to a file
#     with open(output_path, 'w', encoding='utf-8') as out_file:
#         out_file.write(svg_data)
    
#     return output_path

############Trying 2 #############

# import pandas as pd
# from wordcloud import WordCloud
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# import re
# from collections import Counter

# # Download necessary NLTK data
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# def preprocess_text(text):
#     text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphanumeric characters
#     tokens = word_tokenize(text)
#     tokens = [word.lower() for word in tokens]

#     # Remove stop words and additional unnecessary words
#     stop_words = set(stopwords.words('english'))
#     additional_stopwords = {"v", "shall", "may", "etc", "also", "said", "th", "thats"}
#     stop_words.update(additional_stopwords)
#     tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(word) for word in tokens]
#     return tokens

# def generate_word_cloud_from_string(input_string, output_path):
#     # Preprocess the input string
#     preprocessed_tokens = preprocess_text(input_string)
    
#     # Compute word frequencies from the preprocessed string
#     word_frequencies = Counter(preprocessed_tokens)
    
#     # Generate the word cloud using the word frequencies
#     wordcloud = WordCloud(
#         width=1600,
#         height=800,
#         background_color='white',
#         collocations=False,
#         max_font_size=200,  # Adjust the maximum font size
#         margin=10,  # Add margin to prevent words from touching
#         prefer_horizontal=1.0  # Ensure words are placed horizontally
#     )
#     wordcloud.generate_from_frequencies(word_frequencies)
    
#     # Save the word cloud to an SVG file
#     svg_data = wordcloud.to_svg()
#     with open(output_path, 'w', encoding='utf-8') as out_file:
#         out_file.write(svg_data)
    
#     return output_path

# def update_word_frequencies(word_frequencies, new_words):
#     for word in new_words:
#         word_frequencies[word] += 1

# def add_string_to_dataset_and_generate_word_cloud(input_string, csv_path, output_path):
#     # Preprocess the input string
#     preprocessed_tokens = preprocess_text(input_string)
    
#     # Read the existing dataset
#     dataset = pd.read_csv(csv_path)
    
#     # Append the preprocessed string to the 'clean_text' column
#     new_row = pd.DataFrame({'clean_text': [' '.join(preprocessed_tokens)]})
#     dataset = pd.concat([dataset, new_row], ignore_index=True)
    
#     # Save the updated DataFrame to the CSV file
#     dataset.to_csv(csv_path, index=False)
    
#     # Compute word frequencies from the dataset
#     word_frequencies = Counter()
#     for text in dataset['clean_text'].dropna():
#         word_frequencies.update(text.split())
    
#     # Update word frequencies with the new input string
#     update_word_frequencies(word_frequencies, preprocessed_tokens)
    
#     # Generate the word cloud using the updated word frequencies
#     wordcloud = WordCloud(
#         width=1600,
#         height=800,
#         background_color='white',
#         collocations=False,
#         max_font_size=200,  # Adjust the maximum font size
#         margin=10,  # Add margin to prevent words from touching
#         prefer_horizontal=1.0  # Ensure words are placed horizontally
#     )
#     wordcloud.generate_from_frequencies(word_frequencies)
    
#     # Save the word cloud to an SVG file
#     svg_data = wordcloud.to_svg()
#     with open(output_path, 'w', encoding='utf-8') as out_file:
#         out_file.write(svg_data)
    
#     return output_path

# # Example usage
# example_text = """
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

# # Paths to the CSV file and output SVG files
# csv_path = 'modules/legal_merged_dataset.csv'
# output_path_string = 'wordcloud_from_string.svg'
# output_path_dataset = 'wordcloud_from_dataset.svg'

# # Test the functions
# generate_word_cloud_from_string(example_text, output_path_string)
# add_string_to_dataset_and_generate_word_cloud(example_text, csv_path, output_path_dataset)

############# Trying 3 ##################
# import pandas as pd
# from wordcloud import WordCloud
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# import re
# from collections import Counter
# import matplotlib.pyplot as plt

# # Download necessary NLTK data
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# def preprocess_text(text):
#     text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphanumeric characters
#     tokens = word_tokenize(text)
#     tokens = [word.lower() for word in tokens]

#     # Remove stop words and additional unnecessary words
#     stop_words = set(stopwords.words('english'))
#     additional_stopwords = {"v", "shall", "may", "etc", "also", "said", "th", "thats"}
#     stop_words.update(additional_stopwords)
#     tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

#     # Remove short words (length 3 and below)
#     tokens = [word for word in tokens if len(word) > 3]

#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(word) for word in tokens]
#     return tokens

# def generate_word_cloud_from_string(input_string, output_path):
#     # Preprocess the input string
#     preprocessed_tokens = preprocess_text(input_string)
    
#     # Compute word frequencies from the preprocessed string
#     word_frequencies = Counter(preprocessed_tokens)
    
#     # Generate the word cloud using the word frequencies
#     wordcloud = WordCloud(
#         width=1600,
#         height=800,
#         background_color='white',
#         collocations=False,
#         max_words=200,  # Limit the maximum number of words in the cloud
#         contour_width=3,  # Add contour for better visibility
#         contour_color='steelblue',  # Set contour color
#         prefer_horizontal=1.0,  # Ensure words are placed horizontally
#         max_font_size=300,  # Adjust the maximum font size
#         min_font_size=20,  # Adjust the minimum font size
#         scale=5,  # Increase scale for better resolution
#     )
#     wordcloud.generate_from_frequencies(word_frequencies)
    
#     # Save the word cloud to a PNG file with high quality
#     plt.figure(figsize=(16, 8))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     plt.savefig(output_path, format="png", dpi=1000, bbox_inches='tight')
#     plt.close()
    
#     return output_path

# def update_word_frequencies(word_frequencies, new_words):
#     for word in new_words:
#         word_frequencies[word] += 1

# def add_string_to_dataset_and_generate_word_cloud(input_string, csv_path, output_path):
#     # Preprocess the input string
#     preprocessed_tokens = preprocess_text(input_string)
    
#     # Read the existing dataset
#     dataset = pd.read_csv(csv_path)
    
#     # Append the preprocessed string to the 'clean_text' column
#     new_row = pd.DataFrame({'clean_text': [' '.join(preprocessed_tokens)]})
#     dataset = pd.concat([dataset, new_row], ignore_index=True)
    
#     # Save the updated DataFrame to the CSV file
#     dataset.to_csv(csv_path, index=False)
    
#     # Compute word frequencies from the dataset
#     word_frequencies = Counter()
#     for text in dataset['clean_text'].dropna():
#         word_frequencies.update(text.split())
    
#     # Update word frequencies with the new input string
#     update_word_frequencies(word_frequencies, preprocessed_tokens)
    
#     # Generate the word cloud using the updated word frequencies
#     wordcloud = WordCloud(
#         width=1600,
#         height=800,
#         background_color='white',
#         collocations=False,
#         max_words=200,  # Limit the maximum number of words in the cloud
#         contour_width=3,  # Add contour for better visibility
#         contour_color='steelblue',  # Set contour color
#         prefer_horizontal=1.0,  # Ensure words are placed horizontally
#         max_font_size=300,  # Adjust the maximum font size
#         min_font_size=20,  # Adjust the minimum font size
#         scale=5,  # Increase scale for better resolution
#     )
#     wordcloud.generate_from_frequencies(word_frequencies)
    
#     # Save the word cloud to a PNG file with high quality
#     plt.figure(figsize=(16, 8))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     plt.savefig(output_path, format="png", dpi=300, bbox_inches='tight')
#     plt.close()
    
#     return output_path

# # Example usage
# example_text = """
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

# # Paths to the CSV file and output PNG files
# csv_path = 'Datasets/legal_merged_dataset.csv'
# output_path_string = 'Datasets/wordcloud_from_string.png'
# output_path_dataset = 'Datasets/wordcloud_from_dataset.png'

# # Test the functions
# generate_word_cloud_from_string(example_text, output_path_string)
# add_string_to_dataset_and_generate_word_cloud(example_text, csv_path, output_path_dataset)

################TRYING 4####################

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
    df = pd.read_csv(file_path)
    stopwords_list = df[df.columns[0]].tolist()
    return set(stopwords_list)

def preprocess_text(text, stopwords_set):
    text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove non-alphanumeric characters
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords_set]
    return tokens

def generate_word_cloud_from_text(text, stopwords_set, output_path):
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

# File paths
stopwords_path = 'Datasets/stopwords_english.csv'
dataset_path = 'Datasets/legal_merged_dataset.csv'
input_string = """
As the Celtics players and coaches spent the week celebrating leading up to the parade, Brad Stevens was back at the Auerbach Center, working out dozens of prospects they could select in the draft this week. They have the 30th and 54th picks and are over the second apron, so they have to nail it on draft night to help build a sustainable team over the coming years.

That’s why after an evening of popping champagne bottles, the front office was back in the early afternoon to get ready for the future.

“The day after, as much as we were excited and celebratory and everything else, you’re always thinking about what this means for what’s next,” Stevens said. “I think that’s just maybe the coach in me or maybe that’s just my age.”

Stevens made a stir last year when the Celtics traded down multiple times on draft night to accumulate a bevy of future second-round picks while selecting Jordan Walsh with the 38th pick. That is not necessarily going to be the norm for this franchise, particularly since bigger deals for Payton Pritchard and potentially Sam Hauser mean the Celtics need to draft more players who have a chance at making the rotation while they are still on their rookie-scale contracts.

Their long-term depth at center is dubious, considering Al Horford’s age and Kristaps Porziņģis’ forthcoming ankle surgery, expected to happen in the next few weeks.

“Kristaps is still in the middle of consulting with some different doctors and specialists, but we anticipate surgery will be soon,” he said.

Because the second apron takes away most of their roster-building tools beyond signing free agents to minimum contracts, getting a center who can develop into a starter down the road most likely would come through the draft. Xavier Tillman and Luke Kornet are both free agents, while Neemias Queta is still under contract, but those players are all far along in their development track.

That’s why Stevens said they made so many trades last season, since they no longer can aggregate salaries in a trade.

“It’ll be interesting to see how it affects the league,” Stevens said. “Are there a lot less trades? That will be interesting to follow and look back and study over the next couple of years. As far as the picks go, if the right person is available at 30, we will take him.”
"""

# Paths for word cloud images
output_path_string = 'wordcloud_from_string.png'
output_path_dataset = 'wordcloud_from_dataset.png'

# Load stopwords
stopwords_set = load_stopwords(stopwords_path)

# Generate word cloud from the input string
generate_word_cloud_from_text(input_string, stopwords_set, output_path_string)

# Update dataset and generate word cloud from the dataset
update_dataset_and_generate_word_cloud(input_string, dataset_path, stopwords_set, output_path_dataset)
