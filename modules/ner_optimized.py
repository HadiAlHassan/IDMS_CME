# import spacy
# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
# import re

# # Initialize NER model and tokenizer
# ner_model_name = "dslim/bert-large-NER"
# ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
# ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

# # Initialize pipeline
# ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

# # Load SpaCy model for date extraction
# nlp = spacy.load("en_core_web_sm")

# def extract_entities(text):
#     # Split the text into chunks of 150 words
#     words = text.split()
#     chunks = [' '.join(words[i:i+150]) for i in range(0, len(words), 150)]

#     entities = {"Names": set(), "Locations": set(), "Organizations": set(), "Dates": set()}

#     for chunk in chunks:
#         # Perform NER analysis on each chunk
#         ner_results = ner_pipeline(chunk)
#         # print("NER Results for chunk:", ner_results)  # Debug: Print NER results for chunk

#         current_entity = ""
#         current_type = ""

#         # Process NER results
#         for entity in ner_results:
#             entity_text = entity['word']
#             entity_type = entity['entity']

#             if entity_text.startswith("##"):
#                 current_entity += entity_text[2:]
#             else:
#                 if current_entity and current_type:
#                     if current_type == 'B-PER' or current_type == 'I-PER':
#                         entities["Names"].add(current_entity.strip())
#                     elif current_type == 'B-LOC' or current_type == 'I-LOC':
#                         entities["Locations"].add(current_entity.strip())
#                     elif current_type == 'B-ORG' or current_type == 'I-ORG':
#                         entities["Organizations"].add(current_entity.strip())
#                 current_entity = entity_text
#                 current_type = entity_type

#         # Add the last entity
#         if current_entity and current_type:
#             if current_type == 'B-PER' or current_type == 'I-PER':
#                 entities["Names"].add(current_entity.strip())
#             elif current_type == 'B-LOC' or current_type == 'I-LOC':
#                 entities["Locations"].add(current_entity.strip())
#             elif current_type == 'B-ORG' or current_type == 'I-ORG':
#                 entities["Organizations"].add(current_entity.strip())

#         # Use SpaCy to extract dates
#         doc = nlp(chunk)
#         for ent in doc.ents:
#             if ent.label_ == "DATE":
#                 entities["Dates"].add(ent.text)

#     # Filter out unwanted characters and short entities
#     entities["Names"] = {name for name in entities["Names"] if len(name) > 2 and name != '"'}
#     entities["Locations"] = {location for location in entities["Locations"] if len(location) > 2 and location != '"'}
#     entities["Organizations"] = {org for org in entities["Organizations"] if len(org) > 2 and org != '"'}
#     entities["Dates"] = {date for date in entities["Dates"] if len(date) > 2 and date != '"'}

#     # print("Extracted Entities:", entities)  # Debug: Print extracted entities

#     return entities
# example_text="""

# """

# # Extract entities and dates
# extracted_entities = extract_entities(example_text)
# print(extracted_entities)

import re
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Initialize NER model and tokenizer for English
ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

# Initialize pipeline
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple")

def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%B %d, %Y")
    # Remove leading zero from the day
    if formatted_date[5] == '0':
        formatted_date = formatted_date[:5] + formatted_date[6:]
    return formatted_date

def extract_dates(text):
    # Regular expression patterns for various date formats
    date_patterns = [
        # MM/DD/YY, DD/MM/YY, YY/MM/DD
        r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b',
        r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{2,4})\b',
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{2,4})\b',
        r'\b(\d{2,4})[-/](\d{1,2})[-/](\d{1,2})\b',
        r'\b(\d{4})\b',
        
        # Month-Day-Year, Month-Day-Year (no leading zeros)
        r'\b(\d{1,2})[-](\d{1,2})[-](\d{4})\b',
        r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b',
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})\b',
        
        # MMDDYY, DDMMYY, YYMMDD
        r'\b(\d{2})(\d{2})(\d{2})\b',
        r'\b(\d{2})(\d{2})(\d{2})\b',
        r'\b(\d{4})(\d{2})(\d{2})\b',

        # MonDDYY, DDMonYY, YYMonDD
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\d{2})(\d{2})\b',
        r'\b(\d{2})(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\d{2})\b',
        r'\b(\d{4})(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\d{2})\b',

        # Day of year, Year-Day of year
        r'\b(\d{1,3})/(\d{4})\b',
        r'\b(\d{4})/(\d{1,3})\b',

        # D Month, Yr, Yr, Month D
        r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December),\s+(\d{4})\b',
        r'\b(\d{4}),\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\b',

        # Mon-DD-YYYY, DD-Mon-YYYY, YYYY-Mon-DD
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{2})-(\d{4})\b',
        r'\b(\d{2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{4})\b',
        r'\b(\d{4})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{2})\b',

        # Mon DD, YYYY, DD Mon, YYYY, YYYY, Mon DD
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{2}),\s+(\d{4})\b',
        r'\b(\d{2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),\s+(\d{4})\b',
        r'\b(\d{4}),\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{2})\b'
    ]

    dates = set()
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) == 3:
                if pattern in [r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{2,4})\b', r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{2,4})\b']:
                    day, month, year = match[1], match[0], match[2]
                elif pattern in [r'\b(\d{1,2})[-](\d{1,2})[-](\d{4})\b', r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b', r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})\b']:
                    day, month, year = match[0], match[1], match[2]
                else:
                    day, month, year = match[1], match[0], match[2]
            else:
                if pattern in [r'\b(\d{2})(\d{2})(\d{2})\b', r'\b(\d{2})(\d{2})(\d{2})\b', r'\b(\d{4})(\d{2})(\d{2})\b']:
                    day, month, year = match[1], match[2], match[0]
                else:
                    year, month, day = match[0], match[1], match[2] if len(match) == 3 else (None, None, None)

            # Ensure the year is in a reasonable range
            if year and len(year) == 2:
                year = "19" + year if int(year) > 50 else "20" + year
            year = int(year) if year else None
            if 1900 <= year <= 2100:
                try:
                    if day and month:
                        date_str = f"{year:04d}-{int(month):02d}-{int(day):02d}"
                    elif year:
                        # Assign a default month and day for year-only dates
                        date_str = f"{year:04d}-01-01"
                    formatted_date = format_date(date_str)
                    dates.add(formatted_date)
                except ValueError:
                    continue
    return dates

def extract_entities(text):
    # Split the text into chunks of 150 words
    words = text.split()
    chunks = [' '.join(words[i:i+150]) for i in range(0, len(words), 150)]

    entities = {"Names": set(), "Locations": set(), "Organizations": set(), "Dates": set()}

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

        # Use custom date extraction to find dates
        dates = extract_dates(chunk)
        entities["Dates"].update(dates)

    # Combine multi-word entities and separate them correctly
    def combine_entities(entity_set):
        combined_entities = set()
        temp_entity = ""
        for entity in sorted(entity_set):
            if temp_entity and (entity.istitle() or not entity[0].islower()): # Check if it starts with uppercase
                temp_entity += " " + entity
            else:
                if temp_entity:
                    combined_entities.add(temp_entity)
                temp_entity = entity
        if temp_entity:
            combined_entities.add(temp_entity)
        return combined_entities

    def format_entities(entity_set):
        formatted_entities = []
        for entity in sorted(entity_set):
            formatted_entities.append(entity)
        return {", ".join(formatted_entities)}

    entities["Names"] = format_entities(entities["Names"])
    entities["Locations"] = format_entities(entities["Locations"])
    entities["Organizations"] = format_entities(entities["Organizations"])

    return entities

example_text = """
Press Summary
20 June 2024
R (on the application of Finch on behalf of the Weald Action 
Group) (Appellant) v Surrey County Council and others
(Respondents)
[2024] UKSC 20
On appeal from [2022] EWCA Civ 187
Justices: Lord Kitchin, Lord Sales, Lord Leggatt, Lady Rose and Lord Richards
Background to the Appeal
Before planning permission can be granted for a development project which is likely to have 
significant effects on the environment, legislation in the United Kingdom (and many other 
countries) requires an environmental impact assessment (“EIA”) to be carried out.

"""

# Extract entities and dates
extracted_entities = extract_entities(example_text)
print(extracted_entities)
