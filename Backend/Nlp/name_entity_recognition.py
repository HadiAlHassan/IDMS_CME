import re
import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
 
# Initialize NER model and tokenizer for English
ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)
 
# Initialize pipeline
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple")
 
nlp = spacy.load("en_core_web_trf")
 
def extract_dates_with_spacy_and_regex(text):
    # Define refined regex patterns for date formats
    regex_patterns = [
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # e.g., 20/6/2024
        r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # e.g., 20-6-2024
        r'\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{2,4}\b',  # e.g., 5 February 2024
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{2,4}\b',  # e.g., February 5, 2024
        r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}\b',  # e.g., 5 Feb 2024
        r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b',  # e.g., 2024-06-20
        r'\b\d{1,2} \w{3,9} \d{4}\b',  # e.g., 5 July 2024
        r'\b\d{1,2}\s\w{3,9}\s\d{4}\b',  # e.g., 5 July 2024
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b'  # e.g., April 30, 1994
    ]
   
    # Extract dates using regex
    regex_dates = set()
    for pattern in regex_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            regex_dates.add(match)
   
    # Extract dates using spaCy
    doc = nlp(text)
    spacy_dates = set()
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            spacy_dates.add(ent.text)
   
    # Combine results and filter out non-date phrases
    all_dates = regex_dates.union(spacy_dates)
   
    # Additional filtering to exclude phrases that are not actual dates
    filtered_dates = set()
    for date in all_dates:
        if re.match(r'\d{1,2}/\d{1,2}/\d{2,4}', date) or re.match(r'\d{1,2}-\d{1,2}-\d{2,4}', date):
            filtered_dates.add(date)
        elif re.match(r'\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{2,4}', date):
            filtered_dates.add(date)
        elif re.match(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', date):
            filtered_dates.add(date)
        elif re.match(r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}', date):
            filtered_dates.add(date)
        elif re.match(r'\d{1,2} \w{3,9} \d{4}', date):
            filtered_dates.add(date)
        elif re.match(r'(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}', date):
            filtered_dates.add(date)
 
    return filtered_dates
 
def extract_entities(text):
    # Split the text into chunks of 150 words
    words = text.split()
    chunks = [' '.join(words[i:i+150]) for i in range(0, len(words), 150)]
 
    entities = {"Names": set(), "Locations": set(), "Organizations": set()}
 
    for chunk in chunks:
        # Perform NER analysis on each chunk using BERT NER model
        ner_results = ner_pipeline(chunk)
 
        # Process NER results
        current_entity = ""
        current_type = ""
 
        for entity in ner_results:
            entity_text = entity['word']
            entity_type = entity['entity_group']
 
            if entity_text.startswith("##"):
                current_entity += entity_text[2:]
            else:
                if current_entity and current_type:
                    if current_type == 'PER':
                        entities["Names"].add(current_entity.strip())
                    elif current_type == 'LOC':
                        entities["Locations"].add(current_entity.strip())
                    elif current_type == 'ORG':
                        entities["Organizations"].add(current_entity.strip())
                current_entity = entity_text
                current_type = entity_type
 
        # Add the last entity
        if current_entity and current_type:
            if current_type == 'PER':
                entities["Names"].add(current_entity.strip())
            elif current_type == 'LOC':
                entities["Locations"].add(current_entity.strip())
            elif current_type == 'ORG':
                entities["Organizations"].add(current_entity.strip())
 
    # Combine multi-word entities and separate them correctly
    def format_entities(entity_set):
        formatted_entities = []
        for entity in sorted(entity_set):
            if len(entity) > 1:  # Filter out single-letter entities
                formatted_entities.append(entity)
        return formatted_entities
 
    entities["Names"] = format_entities(entities["Names"])
    entities["Locations"] = format_entities(entities["Locations"])
    entities["Organizations"] = format_entities(entities["Organizations"])
 
    return entities
 
def extract_information(text):
    entities = extract_entities(text)
    dates = extract_dates_with_spacy_and_regex(text)
   
    return {
        "Names": entities["Names"],
        "Organizations": entities["Organizations"],
        "Locations": entities["Locations"],
        "Dates": list(dates)
    }