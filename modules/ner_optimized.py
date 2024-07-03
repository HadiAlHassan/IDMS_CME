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
Edison High School
Athletic Contract
1. To be eligible for any team, the student must meet CIF, SUSD and Edison High School eligibility
requirements. SUSD and the State of California require a Grade Point Average (GPA) of 2.00 and the
student athlete must maintain credits towards graduation. Eligibility will be checked each semester.
2. All athletes must pass a physical examination and have it uploaded into FamilyID. The athlete and
parents must sign the emergency information and the player packet signature form. This form needs to be
submitted to FamillyID before the student is allowed to compete.
3. An athlete may change from one sport to another only if he/she has permission from both coaches. An
athlete is not allowed to quit a sport from one season to go out for another sport the next season. The
athlete MUST finish the sport from the previous season.
4. An athlete MUST be in school a minimum of 2 classes in order to participate in a game or practice held
on that day. A legal admit must be presented if the athlete misses any part of school on a game or
practice day in order to be considered for participation.
5. An athlete MUST attend practices in order to play in the games. It is up to the coach and the individual
sports program to determine the discipline for missed practices (see program guidelines)
6. A student athlete will immediately become ineligible and could lose all playing privileges for that season
of sport for any of the following reasons:
A. Quitting a sport without a justifiable reason or consent of the coach.
B. Smoking, drinking, and/or the use of illegal drugs.
C. Acting in a manner that may bring dishonor or shame to the community or school.
D. Fighting or coming off the bench or sideline during any fight on the playing area.
E. Consistent discipline, academic and/or attendance issues.
F. Participation in a non-school sponsored team, such as city league, shall make the athlete ineligible for
a school team of that same sport if the participation is during the season.
**Eligibility may be earned back at the discretion of administration and / or the coach
7. Student-Athletes are representatives of EHS and at all times must conduct themselves in a manner
that reflects positively on their teams, school and community
Failure to comply with any of the requirements stated in this contract will be referred to the
Coach, the Director of Athletics and/or the Administration for appropriate discipline outlined in
our code violations.
Code Violations and Team Disciplinary Action:
1. Smoking/Distribution/Sale or Use of Tobacco Products - First Violation: Ten (10) day suspension
from all scrimmages and contests . A suspended player is required to participate in all practices. Second
Violation: Twenty (20) day suspension from all scrimmages and contests. Third Violation: Will result in
forfeiture of eligibility to participate in athletics for one (1) year from the point of infraction.
2. Smoking/Distribution/Sale or Use of Marijuana or Marijuana Products - First Violation: Ten (10) day
suspension from all scrimmages and contests . A suspended player is required to participate in all
practices. Second Violation: Twenty (20) day suspension from all scrimmages and contests. Third
Violation: Will result in forfeiture of eligibility to participate in athletics for one (1) year from the point of
infraction.
3. Possession of and/or Consumption of Alcohol and Over the Counter Performance Enhancing
Products. First Violation: Ten (10) day suspension from all scrimmages and contests. A suspended player
is required to participate in all practices. Second Violation: Twenty (20) day suspension from all
scrimmages and contests. Third Violation: Will result in forfeiture of eligibility to participate in athletics for
one (1) year from the point of infraction.
4. Fighting- 45 day social probation(suspension interventions document)
5. Theft or Vandalism: to any school property (Home or Away) while under the supervision of a coach
or while representing the school team in any way. First Violation: Ten (10) day suspension from all
scrimmages and contests. A suspended player is required to participate in all practices. Second Violation:
Twenty (20) day suspension from all scrimmages and contests. Third Violation: Will result in forfeiture of
eligibility to participate in athletics for one (1) year from the point of infraction.
6. Conduct Unbecoming or Other Actions or Excessive Misbehavior: that would reflect negatively
upon the team or school. First Violation: Ten (10) day suspension from all scrimmages and contests. A
suspended player is required to participate in all practices. Second Violation: Twenty (20) day suspension
from all scrimmages and contests. Third Violation: Will result in forfeiture of eligibility to participate in
athletics for one (1) year from the point of infraction.(ex. Running to/instigating/recording or being present
at a fight)
7. Cutting Class: If a student is found cutting a class more than once in a day, that student will be
suspended from all activity that same day. That includes practices, as well as scrimmages, games, meets
and matches. If the multiple cuts goes undetected until the next school day, then the suspension will take
effect immediately for that school day
*NOTE: Suspensions will be carried over to the next season of participation
I,(print name)___________________________, have read, understand, and agree to follow the Edison
High school Athletic Contract
_______________________________________ __________________
Student Signature Date
_______________________________________ __________________
Parent Signature Date
"""

# Extract entities and dates
extracted_entities = extract_entities(example_text)
print(extracted_entities)
