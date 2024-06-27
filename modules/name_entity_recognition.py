import spacy
import json

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def extract_entities_from_text(text):
    """
    Extracts named entities from text and categorizes them, removing duplicates.
    
    Args:
        text (str): The input text from which to extract entities.
        
    Returns:
        dict: A dictionary where the keys are entity labels and the values are lists of unique entities of that type.
    """
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        label = ent.label_
        if label not in entities:
            entities[label] = set()  # Use a set to handle duplicates
        entities[label].add(ent.text)
    
    # Convert sets to lists for final output
    entities = {label: list(entity_set) for label, entity_set in entities.items()}
    
    return entities

def extract_entities_from_file(file_path):
    """
    Reads text from a file and extracts named entities, removing duplicates.
    
    Args:
        file_path (str): The path to the text file.
        
    Returns:
        dict: A dictionary where the keys are entity labels and the values are lists of unique entities of that type.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return extract_entities_from_text(text)

# Example usage with a file
entities_from_file = extract_entities_from_file("testBus.txt")
print(json.dumps(entities_from_file, indent=4))
