import pandas as pd
from pathlib import Path



current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'datasets' / 'NLP_Dataset_Cleaned.csv'

ds = pd.read_csv(dataset_path)

legal_labels= ["Contract", "Agreement", "Court Case"]
non_legal_labels= ["Sport","Politics", "Business","Technology"]

ds["category"]= ds["label"].apply(lambda x: 'Legal' if x in legal_labels else "Non-Legal")

ds.to_csv("NLP_Dataset_Cleaned_With_Category.csv", index=False)
