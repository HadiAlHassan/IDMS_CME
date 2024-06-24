from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud
from datasets import load_dataset


dataset = load_dataset("coastalcph/lex_glue", "ledgar")


print(dataset)
print("------------------")

print(dataset['train'][0])
print("------------------")

train_dataset=pd.DataFrame(dataset["train"])
print(train_dataset.isnull().sum()) #No null values
print("------------------")

contract_type_counts = train_dataset['label'].value_counts().sort_index()
print(contract_type_counts)
print("------------------")

#Count occurences of each label
label_counts = train_dataset['label'].value_counts()
plt.figure(figsize=(10, 10))
sns.barplot(x=label_counts.index, y=label_counts.values)
plt.title('Distribution of Labels')
plt.xlabel('Label')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Text column understanding
text_lengths = train_dataset['text'].apply(lambda x: len(x.split()))

avg_text_length = text_lengths.mean()
max_text_length = text_lengths.max()
min_text_length = text_lengths.min()

print(f"Average text length: {avg_text_length:.2f} words")
print(f"Maximum text length: {max_text_length} words")
print(f"Minimum text length: {min_text_length} words")

# Plot distribution of text lengths
plt.figure(figsize=(10, 10))
sns.histplot(text_lengths, bins=30, kde=True)
plt.title('Distribution of Text Lengths')
plt.xlabel('Number of Words')
plt.ylabel('Count')
plt.show()

print("----------------------")
