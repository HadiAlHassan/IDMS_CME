from datasets import load_dataset
import pandas as pd

# Step 1: Load the dataset
ds = load_dataset("umarbutler/open-australian-legal-corpus")

# Step 2: Extract the "text" field from the nested structure in "corpus" column
text_data = [entry['text'] for entry in ds['corpus']]  # Adjust 'text' if needed

# Step 3: Create a DataFrame with 'text' and 'label' columns
df = pd.DataFrame({'text': text_data, 'label': 5})

# Step 4: Save the DataFrame as a CSV file locally
df.to_csv('text_label_dataset.csv', index=False)

# Print the first few rows to verify
print(df.head())


#text_data = ds['context']  # Assuming you're working with the 'train' split

# Step 2: Create a DataFrame with 'text' and 'label' columns
# 'label' column will have a constant value of 5
#df = pd.DataFrame({'text': text_data, 'label': 5})

# Step 3: Save the DataFrame as a CSV file locally
#df.to_csv('text_label_dataset.csv', index=False)

# Now the DataFrame 'df' containing 'text' and 'label' columns with 'label' value of 5
# has been saved as 'text_label_dataset.csv' in your current working directory.
