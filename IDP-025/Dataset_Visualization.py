from datasets import load_dataset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from pathlib import Path

dataset = load_dataset("coastalcph/lex_glue", "ledgar")


# for split in dataset.keys():
#     print(f"Split: {split}")
#     print(dataset[split].to_pandas().head()) 

#Display the features
print(dataset)
print("-------------")
print(dataset['train'].features)
print("-------------")
print("Shape: ",dataset['train'].shape) #Shape:(60000, 2)
print("-------------")

#number of explams in each split
print(f"Train size: {len(dataset['train'])}")
print(f"Validation size: {len(dataset['validation'])}")
print(f"Test size: {len(dataset['test'])}")
print("-------------")

print(dataset.isnull().sum())

# First example in the train split
print(dataset['train'][0])
print("-------------")

#Easier manipulation
df_train = pd.DataFrame(dataset['train'])
df_val = pd.DataFrame(dataset['validation'])
df_test = pd.DataFrame(dataset['test'])

#label distribution & visualization
label_distribution = df_train['label'].value_counts().sort_index()
print(label_distribution)

plt.figure(figsize=(10, 6))
label_distribution.plot(kind='bar')
plt.xlabel('Class')
plt.ylabel('Count')
plt.title('Class Distribution in LEDGAR Train Set')
plt.show()
print("-------------")

#Text lengths
df_train['text_length'] = df_train['text'].apply(len)

print(df_train['text_length'].describe())

# plot of text lengths
df_train['text_length'].hist(bins=50)
plt.xlabel('Text Length')
plt.ylabel('Frequency')
plt.title('Distribution of Text Lengths in Train Set')  #The histogram is right-skewed, most entries are less than 1000 characters, and there are fewer longer entries.
plt.show()
print("-------------")




# # Convert each split to a pandas DataFrame
# train_df = ds['train'].to_pandas()
# validation_df = ds['validation'].to_pandas()
# test_df = ds['test'].to_pandas()

# # Combine all splits into one DataFrame for a holistic view
# df = pd.concat([train_df, validation_df, test_df], ignore_index=True)

# # Display basic statistics
# print(df.describe())

# # Plot class distribution
# plt.figure(figsize=(10, 6))
# sns.countplot(data=df, x='label')
# plt.title('Class Distribution')
# plt.xlabel('Class')
# plt.ylabel('Count')
# plt.show()

# # Calculate text lengths
# df['text_length'] = df['text'].apply(len)

# # Plot text length distribution
# plt.figure(figsize=(10, 6))
# sns.histplot(df['text_length'], bins=50, kde=True)
# plt.title('Text Length Distribution')
# plt.xlabel('Text Length')
# plt.ylabel('Frequency')
# plt.show()

# # Combine all texts into one string
# all_text = ' '.join(df['text'])

# # Generate word cloud
# wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

# # Display the word cloud
# plt.figure(figsize=(10, 6))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.title('Word Cloud of Texts')
# plt.show()

# print(df.head())