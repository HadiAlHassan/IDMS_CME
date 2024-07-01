# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# # Initialize tokenizers and models
# ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
# ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
# ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

# # Initialize NER pipeline
# ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

# def extract_entities(text):
#     # Perform NER analysis
#     ner_results = ner_pipeline(text)
#     print("NER Results:", ner_results)  # Debug: Print NER results
    
#     entities = {"Names": set(), "Locations": set(), "Organizations": set()}

#     current_entity = ""
#     current_type = ""

#     # Process NER results
#     for entity in ner_results:
#         entity_text = entity['word']
#         entity_type = entity['entity']

#         print(f"Entity Text: {entity_text}, Entity Type: {entity_type}")  # Debug: Print entity text and type
        
#         if entity_text.startswith("##"):
#             current_entity += entity_text[2:]
#         else:
#             if current_entity and current_type:
#                 if current_type == 'B-PER' or current_type == 'I-PER':
#                     entities["Names"].add(current_entity)
#                 elif current_type == 'B-LOC' or current_type == 'I-LOC':
#                     entities["Locations"].add(current_entity)
#                 elif current_type == 'B-ORG' or current_type == 'I-ORG':
#                     entities["Organizations"].add(current_entity)
            
#             current_entity = entity_text
#             current_type = entity_type

#     # Add the last entity
#     if current_entity and current_type:
#         if current_type == 'B-PER' or current_type == 'I-PER':
#             entities["Names"].add(current_entity)
#         elif current_type == 'B-LOC' or current_type == 'I-LOC':
#             entities["Locations"].add(current_entity)
#         elif current_type == 'B-ORG' or current_type == 'I-ORG':
#             entities["Organizations"].add(current_entity)
    
#     # Filter out unwanted characters and short entities
#     entities["Names"] = {name for name in entities["Names"] if len(name) > 2 and name != '"'}
#     entities["Locations"] = {location for location in entities["Locations"] if len(location) > 2 and location != '"'}
#     entities["Organizations"] = {org for org in entities["Organizations"] if len(org) > 2 and org != '"'}

#     print("Extracted Entities:", entities)  # Debug: Print extracted entities
    
#     return entities

# # Example usage with a text
# example_text = """
# HOW TO BRIEF A CASE 
# The cases that you will read are the written opinions of trial and appellate court 
# judges explaining their decisions in the lawsuit. A court opinion is similar to a short 
# story of an incident in which a court acted to resolve a legal dispute. The opinions are a 
# record of the court’s decisions that will be used as precedents to provide authority or 
# guidance in resolving future legal disputes. 
# Case briefing is an aid in reading and understanding court opinions. The process 
# is actually a very familiar task to you – it involves outlining and making notes about what 
# you read by identifying the parts of a case and summarizing them. Case briefs will be 
# useful to you in preparing for class and in reviewing for exams. After you have read a 
# case, re-read and brief it using the following format for briefing a case. 
# 1. Name of Case 
#  Write the name of the case at the beginning of your brief so that you will be able 
# to identify it later. The case name usually contains the names of the plaintiff and the 
# defendant, who are the parties to the lawsuit. Be sure that you can identify who sued and 
# who was sued as you read through the case. 
# 2. Facts 
#  Briefly summarize the facts of the case. Facts are the “who, when, what, where, 
# and why” of the case. Describe the history of the dispute, including the events that led to 
# the lawsuit, the legal claims and defenses of each party, and what happened in the trial 
# court. Do not merely copy the facts verbatim; not every detail is important. Instead, 
# include only the relevant facts. To decide which facts are relevant, ask yourself whether 
# a particular fact was important to the court’s decision. If the answer is yes, include that 
# fact in your brief. You can also ask yourself whether the court’s decision may have been 
# different if a particular fact was omitted or changed. If so, then it is important. You 
# should also look for facts that are repeated at least once in the court’s opinion since these 
# tend to be legally relevant. 
# 3. Issue(s) 
#  The issue is a statement of the question of law that the court must answer in order 
# to decide which party should win. A case may involve more than one issue. Sometimes 
# the court will directly state the issue in the opinion. If so, then you can quote the court’s 
# statement of the issue in your brief. In most cases, however, you will need to write your 
# own statement of the issue. The issue should be expressed in the form of a question that 
# can be answered “yes” or “no”. To ensure that your issue statements are written in the 
# form of a question, begin them with “whether,” “did,” “can,” “does,” “is,” etc. 
# 4. Holding(s) 
#  The holding is the answer to the issue. If there are multiple issues, then you 
# should state a holding for each issue. The holding succinctly states the court’s ultimate 
# conclusion, but does not fully explain the conclusion. Write the holding as a single 
# sentence that begins with “yes” or “no,” followed by the word “because.” Doing this will 
# ensure that you directly answer the issue and provide a brief reason for the court’s 
# conclusion. 
# 5. Rationale 
#  The court must justify its holding by providing reasons for answering the issue in 
# the way that it did. The rationale is a summary of the reasons that explain how the court 
# reached its decision. The goal for this part of your brief is to understand how the court 
# used the rules of law to resolve the dispute. The court will state the applicable rules of 
# law, and they can be found in readings from your textbook as well. You should 
# summarize how the court applied the rules to the facts to reach its conclusions. 
#  After you have finished briefing a case, take a moment to critically evaluate the 
# court’s decision. Ask yourself whether you agree with the outcome. Is the outcome fair 
# in light of the facts and the law? Has the court considered all of the relevant facts? Do 
# you agree with the court’s reasoning? What is the likely impact of the decision in the 
# business environment? 
# There are different approaches to briefing each aspect of the case that work 
# equally well. You can write your brief in narrative form or simply list the facts, issues, 
# holdings, and reasons as bullet points in your brief. The key is to create a complete 
# summary of the court’s opinion. Remember also: case briefs should be brief. A good 
# rule of thumb is no more than one page for most cases. 
# To practice briefing a case using the method described above, read the following 
# case of Hagan v. Adams Property Associates, Inc. The case involves a limited liability 
# company, or LLC, which is a type of business where the owners manage the business but 
# have limited legal liability as to business debts and obligations. After you have read the 
# Hagan case, re-read it while referring to the sample case brief that follows. As you do so, 
# critically evaluate the outcome of the case and the reasoning behind the court’s decision. 
# Consider whether or not you agree with the court’s decision. 
# HAGAN v. ADAMS PROPERTY ASSOCIATES, INC. 
# 482 S.E.2d 805 (Va. 1997) 
# Ralph E. Hagan (Hagan) owned the Stuart Court Apartments (the property) in Richmond, 
# Virginia. On April 30, 1994, Hagan signed an agreement with Adams Property Associates, Inc. 
# (Adams), giving Adams the exclusive right to sell the property for $1,600,000. The agreement 
# provided that if the property was “sold or exchanged” within one year, with or without Adams’ 
# assistance, Hagan would pay Adams a commission of six percent of the “gross sales amount.” 
# Before the year expired, Hagan, Roy T. Tepper, and Lynn Parsons formed a limited liability 
# company, known as Hagan, Parsons, & Tepper, L.L.C. (HPT). By deed dated April 23, 1995, 
# Hagan transferred the property to HPT. Adams believed that the transfer of the property to HPT 
# constituted a sale of the property and asked Hagan to pay him the six percent commission as 
# provided in their agreement. When Hagan refused, Adams filed suit against Hagan seeking 
# recovery of the commission. The trial court held that Adams was entitled to a commission and 
# Hagan appealed. 
# Lacy, Justice. In this appeal, we consider 
# whether a transfer of real property from its 
# owner to a limited liability company in 
# which the owner is a member constitutes the 
# sale of the property, entitling a real estate 
# broker to a commission authorized by a 
# listing agreement between the owner and 
# broker. 
#  Hagan first contends that transfer of legal 
# title to the property to HPT did not 
# constitute a sale. We disagree. Whether a 
# particular transaction constitutes a sale is a 
# matter of law to be determined by the 
# court. In a number of previous cases, we 
# have determined that a sale is effected 
# when a transfer of property occurs in 
# exchange for valuable consideration. We 
# have recognized that valuable consideration 
# can take different forms. In this case, the 
# trial court concluded that the mutual 
# promises between Hagan and his associates 
# constituted valuable consideration 
# sufficient to effect a sale of the property to 
# HPT, thus entitling Adams to a 
# commission. We agree and will affirm the 
# trial court's decision.
# """

# # Extract entities
# entities = extract_entities(example_text)
# print(entities)

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