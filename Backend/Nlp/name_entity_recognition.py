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

