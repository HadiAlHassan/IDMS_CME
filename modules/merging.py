import pandas as pd

# Load the three datasets
dataset1 = pd.read_csv('Datasets/nltk_eng_stopwords.csv')
dataset2 = pd.read_csv('Datasets/stopwords.csv')
dataset3 = pd.read_csv('Datasets/all_english_vocabulary.csv')

# Rename the columns to a common name 'stopwords'
dataset1 = dataset1.rename(columns={'list_of_stopwords': 'stopwords'})
dataset2 = dataset2.rename(columns={'stopwords': 'stopwords'})
dataset3 = dataset3.rename(columns={'0': 'stopwords'})

# Combine the datasets
combined_dataset = pd.concat([dataset1, dataset2, dataset3], ignore_index=True)

# Drop duplicate rows
combined_dataset = combined_dataset.drop_duplicates()
combined_dataset = combined_dataset.dropna()

# Save the final dataset to a CSV file
combined_dataset.to_csv('stopwords_english.csv', index=False)

print("Datasets merged and saved to 'stopwords_english.csv'")
