import pandas as pd
from pathlib import Path
from sklearn.utils import shuffle

Legal_dataset=pd.read_csv("Legal_dataset.csv")

current_dir = Path(__file__).resolve().parent
dataset_path = current_dir.parent / 'Datasets' / 'Non_legal_dataset.csv'

Non_Legal_dataset= pd.read_csv(dataset_path)

Legal_dataset.columns = map(str.lower, Legal_dataset.columns)
Non_Legal_dataset.columns = map(str.lower, Non_Legal_dataset.columns)

print(Legal_dataset.head())
print("-----------------------")
print(Non_Legal_dataset.head())
print("-----------------------")

Legal_Non_Legal= pd.concat([Legal_dataset, Non_Legal_dataset])

Legal_Non_Legal=shuffle(Legal_Non_Legal)

print(Legal_Non_Legal.head())

Legal_Non_Legal.to_csv("Legal_Non_Legal_Dataset.csv", index=False)