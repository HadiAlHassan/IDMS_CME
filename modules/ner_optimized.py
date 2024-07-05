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
            formatted_entities.append(entity)
        return {", ".join(formatted_entities)}

    entities["Names"] = format_entities(entities["Names"])
    entities["Locations"] = format_entities(entities["Locations"])
    entities["Organizations"] = format_entities(entities["Organizations"])

    return entities

example_text = """
GENERAL GUIDANCE ON PDF BUNDLES
This guidance is provided in order to achieve a level of useful consistency in the provision of 
PDF bundles for use by judges in hearings. It is not immutable, and should give way to any 
specific directions by particular courts or the requirements of particular judges in particular 
cases. However, it should, if operated properly, provide judges with bundles which are as 
useful as they can be made. It should be provided to solicitors and litigants in person as a 
guide to the construction of useful bundles. They ought to be able to comply with all or 
most of these requirements. If they cannot they should explain why.
However, please note that these notes are not intended for use in the tribunals.
Bundling should follow the following principles:
1. All bundles must, where the character of the document permits, be the subject of OCR
(optical character recognition). This is the process which turns the document from a mere 
picture of a document to one in which the text can be read as text so that the document 
becomes word-searchable and words can be highlighted in the process of marking them up. 
It is acknowledged that some individual documents may not be susceptible to the process, 
but most should be.
2. All documents should appear in portrait mode. If an original document is in landscape, 
then it should be inserted so that it can be read with a 90 degree rotation clockwise. No 
document should appear upside down.
3. The default view for all pages should be 100%.
4. If a core bundle is required under normal practice, then a PDF core bundle should be 
produced complying with the same requirements as a paper bundle.
5. Proper thought should be given to the number of bundles required. It is generally not 
helpful to have to open a significant number of PDF files during the course of a hearing in 
order to get at documents. In very many cases it will doubtless be possible to combine all 
documents in one bundle – statements of case, witness statements and other documents
(this is the preference of the Family Courts). In larger cases it may be sensible to separate 
out those categories of documents into separate bundles. However, further subdivision is 
not helpful – eg it is not helpful to have separate witness statements in separate PDF files. 
Generally speaking a chronological run of documents should be in one overall file. Again 
generally speaking, authorities should always be provided in a separate file; this file should 
be page numbered like all others – see below.
6. All pages in a bundle must be numbered, and if possible by a computer generated 
numbering, or at least in typed form (if added by a scanner), and not numbered by hand. If 
computer generated or typed the number becomes machine readable and can be searched 
for. Again if possible, the number should be preceded by a letter, whether the letter of the 
bundle or not. This aids searching. For example, it will be quick to search for and go to page 
A134 by searching for that. Searching for just “134” may throw up a number of references 
to that number which are not the page number, which takes the computer time.
7. Pagination should not mask relevant detail on the original document.
8. If practicable any scans of documents should not be greater than 300 dpi, in order to 
avoid slow scrolling or rendering.
9. All significant documents and all sections in bundles must be bookmarked for ease of 
navigation, with an appropriate description as the bookmark. The bookmark should contain 
the page number of the document.
10. An index or table of contents of the documents should be prepared. If practicable 
entries should be hyperlinked to the indexed document. Common sense will usually dictate 
the level of detail in this table of contents.
11. All PDF files must contain a short version of the name of the case and an indication of 
the number/letter of the bundle, and end with the hearing date. For example “Carpenters
v Adventurers Bundle B 1-4-20”; or “Carpenters v Adventures correspondence 1-4-20”. 
They must not be labelled simply “Correspondence” or “Bundle B”.
12. If a bundle is to be added to after the file has been transmitted to the judge it should 
not be assumed the judge will accept it as a complete replacement because he/she may 
already have started to mark up the original. Inquiries should be made of the judge as to 
what the judge would like to do about it. Absent a particular direction, a substitute bundle 
should be made available, but any pages to be added should also be provided separately, in 
a separate file, as well, with pages appropriately sub-numbered (143.1, 143.2 etc).
13. In Family Proceedings any bundle must meet the requirements set out in FPR 2010, 
PD27A.
Delivering e-bundles
If an e-bundle is to be delivered by email the sender must be aware that there is a maximum 
size of attached files which can be received by a justice.gov (DOM1) address. It is 36Mb in 
aggregate. An email with an attached file which is bigger than that, or an email with files 
which together total more than that in size, will be rejected. The maximum size of the 
attachments sent to an ejudiciary.net address is 150Mb in aggregate. The latter limit is 
seldom likely to cause a problem, though a court-side recipient may not have an Ejudiciary 
account. The former may. The solution may be to transmit bundles by separate emails. 
Unless it is absolutely necessary the temptation to break sensibly bundled documents into 
smaller bundles just for the purpose of transmission should be avoided.
If bundles are transmitted by email the email subject line should provide the following 
detail:
(a) Case number;
(b) Case name (shortest comprehensible version);
(c) Hearing date;
(d) Judge Name (if known);
(e) The words in capitals “REMOTE HEARING”.
An alternative is to have documents submitted by a file uploading/downloading system. It is 
known that some solicitors are using commercial services which provide for that. HMCTS is 
shortly to launch its own service; details will be provided separately, and it is likely that 
solicitors will be encouraged to use that service.
Litigants in person 
An e-bundle is an organised collection of electronic copies of documents for use at a court 
hearing that is to take place remotely (by video link or by telephone).
Ordinarily the applicant is responsible for preparing the e-bundle. If a litigant in person is 
the applicant the e-bundle must still if at all possible, comply with the above requirements. 
If it is not possible for a litigant in person to comply with the requirements on e-bundles, a 
brief explanation of the reasons for this should be provided to the court as far in advance of 
the hearing as possible. Where possible the litigant in person should identify a practical way 
of overcoming the problem so that the court can consider this.
In a case in which a litigant in person is applicant and another party has legal representation 
the legal representatives for other party should consider offering to prepare the e-bundle. 
The litigant in person will still be entitled to indicate which documents they consider 
necessary for inclusion in the e-bundle. 
Litigants in person who are not eligible for legal aid or cannot access legal aid (publiclyfunded legal assistance) and who do not have the financial means to engage legal assistance 
may wish to consider approaching an advice centre, law centre or pro bono organisation to 
see whether legal assistance can be made available without charge. Some but not all advice 
centres, law centres and pro bono organisations can now be reached on-line or by 
telephone. 
Other internet guidance
Amongst the other internet guidance which is generally available, the following guides 
might be thought to be particularly useful because of their links with the legal profession:
(a) A QEB guide to creating an e-bundle - see this YouTube video;
(b) A video prepared by St Philips Chambers on creating a bundle using Adobe Acrobat 
Pro: https://st-philips.com/creating-and-using-electronic-hearing-bundles/
Future versions of this guidance
This document is intended to be a living document which is to be revised from time to time 
in the light of experience. It will therefore be useful to check back with it from time to time.
Sir Andrew McFarlane
President of the Family Division
Lady Justice Thirlwall
Senior Presiding Judge
Mr Justice Mann
Judge in charge of Live Services

"""

# Extract entities and dates
extracted_entities = extract_entities(example_text)
print(extracted_entities)
extracted_dates = extract_dates_with_spacy_and_regex(example_text)

print("Dates: ",extracted_dates)