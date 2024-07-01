import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re

# Initialize NER model and tokenizer
ner_model_name = "dslim/bert-large-NER"
ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

# Initialize pipeline
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

# Load SpaCy model for date extraction
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    # Split the text into chunks of 150 words
    words = text.split()
    chunks = [' '.join(words[i:i+150]) for i in range(0, len(words), 150)]

    entities = {"Names": set(), "Locations": set(), "Organizations": set(), "Dates": set()}

    for chunk in chunks:
        # Perform NER analysis on each chunk
        ner_results = ner_pipeline(chunk)
        # print("NER Results for chunk:", ner_results)  # Debug: Print NER results for chunk

        current_entity = ""
        current_type = ""

        # Process NER results
        for entity in ner_results:
            entity_text = entity['word']
            entity_type = entity['entity']

            if entity_text.startswith("##"):
                current_entity += entity_text[2:]
            else:
                if current_entity and current_type:
                    if current_type == 'B-PER' or current_type == 'I-PER':
                        entities["Names"].add(current_entity.strip())
                    elif current_type == 'B-LOC' or current_type == 'I-LOC':
                        entities["Locations"].add(current_entity.strip())
                    elif current_type == 'B-ORG' or current_type == 'I-ORG':
                        entities["Organizations"].add(current_entity.strip())
                current_entity = entity_text
                current_type = entity_type

        # Add the last entity
        if current_entity and current_type:
            if current_type == 'B-PER' or current_type == 'I-PER':
                entities["Names"].add(current_entity.strip())
            elif current_type == 'B-LOC' or current_type == 'I-LOC':
                entities["Locations"].add(current_entity.strip())
            elif current_type == 'B-ORG' or current_type == 'I-ORG':
                entities["Organizations"].add(current_entity.strip())

        # Use SpaCy to extract dates
        doc = nlp(chunk)
        for ent in doc.ents:
            if ent.label_ == "DATE":
                entities["Dates"].add(ent.text)

    # Filter out unwanted characters and short entities
    entities["Names"] = {name for name in entities["Names"] if len(name) > 2 and name != '"'}
    entities["Locations"] = {location for location in entities["Locations"] if len(location) > 2 and location != '"'}
    entities["Organizations"] = {org for org in entities["Organizations"] if len(org) > 2 and org != '"'}
    entities["Dates"] = {date for date in entities["Dates"] if len(date) > 2 and date != '"'}

    # print("Extracted Entities:", entities)  # Debug: Print extracted entities

    return entities
example_text="""


"""

# Extract entities and dates
extracted_entities = extract_entities(example_text)
print(extracted_entities)