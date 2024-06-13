import spacy
from pathlib import Path

nlp = spacy.load('en_core_web_sm')

current_dir=Path(__file__).resolve().parent

file1_name=input("Enter the first file name: ") + ".txt"
file2_name=input("Enter the second file name: ") + ".txt"

file1_path=current_dir / 'TestingTxtFiles'/ file1_name
file2_path=current_dir / 'TestingTxtFiles'/file2_name

with open(file1_path, 'r', encoding='utf-8') as file1:
    file1_content = file1.read()

with open(file2_path, 'r', encoding='utf-8') as file2:
    file2_content = file2.read()

doc1 = nlp(file1_content)
doc2 = nlp(file2_content)

# filtered_tokens1 = [token.text for token in doc1 if not token.is_stop and not token.is_punct]
# filtered_text1 = ' '.join(filtered_tokens1)

# for ent in doc1.ents:
#   print(f"{ent.ents} ({ent.label_})")

# filtered_tokens2 = [token.text for token in doc2 if not token.is_stop and not token.is_punct]
# filtered_text2= ' '.join(filtered_tokens2)


similarity = doc1.similarity(doc2)
print(f"The similarity between the documents is: {similarity:.4f}")