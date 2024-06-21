from datasets import load_dataset
import pandas as pd

# Step 1: Load the dataset and extract the "text" column
ds = pd.read_csv("Legal_dataset.csv")
  # Assuming you're working with the 'train' split

# Step 2: Create a DataFrame with 'text' and 'label' columns
# 'label' column will have a constant value of 5
df = pd.DataFrame({'text': ds['text'], 'label': 5})

# Step 3: Save the DataFrame as a CSV file locally
df.to_csv('Legal_dataset.csv', index=False)