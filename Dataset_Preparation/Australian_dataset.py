from datasets import load_dataset
import pandas as pd

#Load the dataset
ds = load_dataset("umarbutler/open-australian-legal-corpus")

#Extract the "text" field from the nested structure in "corpus" column
text_data = [entry['text'] for entry in ds['corpus']]  # Adjust 'text' if needed

# Create a DataFrame with 'text' and 'label' columns
df = pd.DataFrame({'text': text_data, 'label': 5})

#Save the DataFrame as a CSV file locally
df.to_csv('text_label_dataset.csv', index=False)

# Print the first few rows
print(df.head())