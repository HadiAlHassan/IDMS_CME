# import re
# import spacy
# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# # Initialize NER model and tokenizer for English
# ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
# ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
# ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

# # Initialize pipeline
# ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer, aggregation_strategy="simple")

# nlp = spacy.load("en_core_web_trf")

# def extract_dates_with_spacy_and_regex(text):
#     # Define refined regex patterns for date formats
#     regex_patterns = [
#         r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # e.g., 20/6/2024
#         r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # e.g., 20-6-2024
#         r'\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{2,4}\b',  # e.g., 5 February 2024
#         r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{2,4}\b',  # e.g., February 5, 2024
#         r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}\b',  # e.g., 5 Feb 2024
#         r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b',  # e.g., 2024-06-20
#         r'\b\d{1,2} \w{3,9} \d{4}\b',  # e.g., 5 July 2024
#         r'\b\d{1,2}\s\w{3,9}\s\d{4}\b',  # e.g., 5 July 2024
#         r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b'  # e.g., April 30, 1994
#     ]
    
#     # Extract dates using regex
#     regex_dates = set()
#     for pattern in regex_patterns:
#         matches = re.findall(pattern, text)
#         for match in matches:
#             regex_dates.add(match)
    
#     # Extract dates using spaCy
#     doc = nlp(text)
#     spacy_dates = set()
#     for ent in doc.ents:
#         if ent.label_ == 'DATE':
#             spacy_dates.add(ent.text)
    
#     # Combine results and filter out non-date phrases
#     all_dates = regex_dates.union(spacy_dates)
    
#     # Additional filtering to exclude phrases that are not actual dates
#     filtered_dates = set()
#     for date in all_dates:
#         if re.match(r'\d{1,2}/\d{1,2}/\d{2,4}', date) or re.match(r'\d{1,2}-\d{1,2}-\d{2,4}', date):
#             filtered_dates.add(date)
#         elif re.match(r'\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{2,4}', date):
#             filtered_dates.add(date)
#         elif re.match(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', date):
#             filtered_dates.add(date)
#         elif re.match(r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}', date):
#             filtered_dates.add(date)
#         elif re.match(r'\d{1,2} \w{3,9} \d{4}', date):
#             filtered_dates.add(date)
#         elif re.match(r'(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}', date):
#             filtered_dates.add(date)

#     return filtered_dates

# def extract_entities(text):
#     # Split the text into chunks of 150 words
#     words = text.split()
#     chunks = [' '.join(words[i:i+150]) for i in range(0, len(words), 150)]

#     entities = {"Names": set(), "Locations": set(), "Organizations": set()}

#     for chunk in chunks:
#         # Perform NER analysis on each chunk using BERT NER model
#         ner_results = ner_pipeline(chunk)

#         # Process NER results
#         current_entity = ""
#         current_type = ""

#         for entity in ner_results:
#             entity_text = entity['word']
#             entity_type = entity['entity_group']

#             if entity_text.startswith("##"):
#                 current_entity += entity_text[2:]
#             else:
#                 if current_entity and current_type:
#                     if current_type == 'PER':
#                         entities["Names"].add(current_entity.strip())
#                     elif current_type == 'LOC':
#                         entities["Locations"].add(current_entity.strip())
#                     elif current_type == 'ORG':
#                         entities["Organizations"].add(current_entity.strip())
#                 current_entity = entity_text
#                 current_type = entity_type

#         # Add the last entity
#         if current_entity and current_type:
#             if current_type == 'PER':
#                 entities["Names"].add(current_entity.strip())
#             elif current_type == 'LOC':
#                 entities["Locations"].add(current_entity.strip())
#             elif current_type == 'ORG':
#                 entities["Organizations"].add(current_entity.strip())

#     # Combine multi-word entities and separate them correctly
#     def format_entities(entity_set):
#         formatted_entities = []
#         for entity in sorted(entity_set):
#             if len(entity) > 1:  # Filter out single-letter entities
#                 formatted_entities.append(entity)
#         return {", ".join(formatted_entities)}

#     entities["Names"] = format_entities(entities["Names"])
#     entities["Locations"] = format_entities(entities["Locations"])
#     entities["Organizations"] = format_entities(entities["Organizations"])

#     return entities


# example_text = """
# GENERAL GUIDANCE ON PDF BUNDLES
# This guidance is provided in order to achieve a level of useful consistency in the provision of 
# PDF bundles for use by judges in hearings. It is not immutable, and should give way to any 
# specific directions by particular courts or the requirements of particular judges in particular 
# Mr Justice Mann
# Judge in charge of Live Services

# """

# # Extract entities and dates
# extracted_entities = extract_entities(example_text)
# print(extracted_entities)
# extracted_dates = extract_dates_with_spacy_and_regex(example_text)

# print("Dates: ",extracted_dates)

#################

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
            regex_dates.add(match.lower())
    
    # Extract dates using spaCy
    doc = nlp(text)
    spacy_dates = set()
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            spacy_dates.add(ent.text.lower())
    
    # Combine results and filter out non-date phrases
    all_dates = regex_dates.union(spacy_dates)
    
    # Additional filtering to exclude phrases that are not actual dates
    filtered_dates = set()
    for date in all_dates:
        if re.match(r'\d{1,2}/\d{1,2}/\d{2,4}', date) or re.match(r'\d{1,2}-\d{1,2}-\d{2,4}', date):
            filtered_dates.add(date)
        elif re.match(r'\d{1,2} (?:january|february|march|april|may|june|july|august|september|october|november|december) \d{2,4}', date):
            filtered_dates.add(date)
        elif re.match(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', date):
            filtered_dates.add(date)
        elif re.match(r'\d{1,2} (?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) \d{2,4}', date):
            filtered_dates.add(date)
        elif re.match(r'\d{1,2} \w{3,9} \d{4}', date):
            filtered_dates.add(date)
        elif re.match(r'(?:january|february|march|april|may|june|july|august|september|october|november|december) \d{1,2}, \d{4}', date):
            filtered_dates.add(date)

    return list(filtered_dates)

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
                        entities["Names"].add(current_entity.strip().lower())
                    elif current_type == 'LOC':
                        entities["Locations"].add(current_entity.strip().lower())
                    elif current_type == 'ORG':
                        entities["Organizations"].add(current_entity.strip().lower())
                current_entity = entity_text
                current_type = entity_type

        # Add the last entity
        if current_entity and current_type:
            if current_type == 'PER':
                entities["Names"].add(current_entity.strip().lower())
            elif current_type == 'LOC':
                entities["Locations"].add(current_entity.strip().lower())
            elif current_type == 'ORG':
                entities["Organizations"].add(current_entity.strip().lower())

    # Combine multi-word entities and separate them correctly
    def format_entities(entity_set):
        formatted_entities = []
        for entity in sorted(entity_set):
            if len(entity) > 1:  # Filter out single-letter entities
                formatted_entities.append(entity.title())  # Capitalize each entity
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
        "Dates": dates
    }

example_text = """
Supreme Court of United States.

Argued January 27, 1904.
Decided February 23, 1904.
ERROR TO THE SUPREME COURT OF THE STATE OF NEW YORK.
*589 Mr. L. Laflin Kellogg, with whom Mr. Alfred C. Pette was on the brief, for plaintiff in error.

Mr. Howard S. Gans, with whom Mr. William Travers Jerome was on the brief, for defendants in error.

*594 MR. JUSTICE DAY, after making the foregoing statement, delivered the opinion of the court.

We do not feel called upon to discuss the contention that the Fourteenth Amendment has made the provisions of the Fourth and Fifth Amendments to the Constitution of the United States, so far as they relate to the right of the people to be secure against unreasonable searches and seizures and protect them against being compelled to testify in a criminal case against themselves, privileges and immunities of citizens of the United States of which they may not be deprived by the action of the States. An examination of this record convinces us that there has been no violation of these constitutional restrictions, either in an unreasonable search or seizure, or in compelling the plaintiff in error to testify against himself.

No objection was taken at the trial to the introduction of the testimony of the officers holding the search warrant as to the seizure of the policy slips; the objection raised was to receiving in evidence certain private papers. These papers became important as tending to show the custody by the plaintiff in error, with knowledge, of the policy slips. The question was not made in the attempt to resist an unlawful seizure of the private papers of the plaintiff in error, but arose upon objection to the introduction of testimony clearly competent as tending to establish the guilt of the accused of the offense charged. In such cases the weight of authority as well as reason limits the inquiry to the competency of the proffered testimony, and the courts do not stop to inquire as to the means by which the evidence was obtained. The rule is thus laid down in Greenleaf, vol. 1, sec. 254a:

*595 "It may be mentioned in this place that though papers and other subjects of evidence may have been illegally taken from the possession of the party against whom they are offered or otherwise unlawfully obtained, this is no valid objection to their admissibility if they are pertinent to the issue. The court will not take notice how they were obtained, whether lawfully or unlawfully, nor will it form an issue to determine that question."

The author is supported by numerous cases. Of them, perhaps the leading one is Commonwealth v. Dana, 2 Met. (Mass.) 329, in which the opinion was given by Mr. Justice Wilde, in the course of which he said:

"There is another conclusive answer to all these objections. Admitting that the lottery tickets and material were illegally seized, still this is no legal objection to the admission of them in evidence. If the search warrant were illegal, or if the officer serving the warrant exceeded his authority, the party on whose complaint the warrant issued, or the officer, would be responsible for the wrong done; but this is no good reason for excluding the papers seized as evidence, if they were pertinent to the issue, as they unquestionably were. When papers are offered in evidence the court can take no notice how they were obtained, whether lawfully or unlawfully; nor would they form a collateral issue to determine that question. This point was decided in the cases of Leggatt v. Tallervey, 14 East, 302, and Jordan v. Lewis, 14 East, 306 note, and we are entirely satisfied that the principle on which these cases were decided is sound and well established."

This principle has been repeatedly affirmed in subsequent cases by the Supreme Judicial Court of Massachusetts, among others Commonwealth v. Tibbetts, 157 Massachusetts, 519. In that case a police officer, armed with a search warrant calling for a search for intoxicating liquors upon the premises of the defendant's husband, took two letters which he found at the time. Of the competency of this testimony the court said:

"But two points have been argued. The first is that the criminatory articles and letters found by the officer in the defendant's possession were not admissible in evidence, because *596 the officer had no warrant to search for them, and his only authority was under a warrant to search her husband's premises for intoxicating liquors. The defendant contends that under such circumstances the finding of criminatory articles or papers can only be proved when by express provision of statute the possession of them is itself made criminal. This ground of distinction is untenable. Evidence which is pertinent to the issue is admissible, although it may have been procured in an irregular or even in an illegal manner. A trespasser may testify to pertinent facts observed by him, or may put in evidence pertinent articles or papers found by him while trespassing. For the trespass he may be held responsible civilly, and perhaps criminally; but his testimony is not thereby rendered incompetent." Commonwealth v. Acton, 165 Massachusetts, 11; Commonwealth v. Smith, 166 Massachusetts, 370.

To the same effect are Chastang v. State, 83 Alabama, 29; State v. Flynn, 36 N.H. 64. In the latter case it was held:

"Evidence obtained by means of a search warrant is not inadmissible, either upon the ground that it is in the nature of admissions made under duress, or that it is evidence which the defendant has been compelled to furnish against himself, or on the ground that the evidence has been unfairly or illegally obtained, even if it appears that the search warrant was illegally issued." State v. Edwards, 51 W. Va. 220; Shields v. State, 104 Alabama, 35; Bacon v. United States, 97 Fed. Rep. 35; State v. Atkinson, 40 S. Car. 363; Williams v. State, 100 Georgia, 511; State v. Pomeroy, 130 Missouri, 489; Gindrat v. The People, 138 Illinois, 103; Trask v. The People, 151 Illinois, 523; Starchman v. State, 62 Arkansas, 538.

In this court it has been held that if a person is brought within the jurisdiction of one State from another, or from a foreign country, by the unlawful use of force, which would render the officer liable to a civil action or in a criminal proceeding because of the forcible abduction, such fact would not prevent the trial of the person thus abducted in the State wherein he had committed an offence. Ker v. Illinois, 119 U.S. 436; Mahon v. Justice, 127 U.S. 700. The case most relied upon in argument by plaintiff in error is the leading one *597 of Boyd v. United States, 116 U.S. 616. In that case a section of the customs and revenue laws of the United States authorized the court in revenue cases, on motion of the government's attorney, to require the production by the defendant of certain books, records and papers in court, otherwise the allegation of the government's attorney as to their contents to be taken as true. It was held that the act was unconstitutional and void as applied to a suit for a penalty or a forfeiture of the party's goods. The case has been frequently cited by this court and we have no wish to detract from its authority. That case presents the question whether one can be compelled to produce his books and papers in a suit which seeks the forfeiture of his estate on pain of having the statements of government's counsel as to the contents thereof taken as true and used as testimony for the government. The court held in an opinion by Mr. Justice Bradley that such procedure was in violation of both the Fourth and Fifth Amendments; the Chief Justice and Justice Miller held that the compulsory production of such documents did not come within the terms of the Fourth Amendment as an unreasonable search or seizure, but concurred with the majority in holding that the law was in violation of the Fifth Amendment. This case has been cited and distinguished in many of the cases from the state courts which we have had occasion to examine.

The Supreme Court of the State of New York, before which the defendant was tried, was not called upon to issue process or make any order calling for the production of the private papers of the accused, nor was there any question presented as to the liability of the officer for the wrongful seizure, or of the plaintiff in error's right to resist with force the unlawful conduct of the officer, but the question solely was, were the papers found in the execution of the search warrant, which had a legal purpose in the attempt to find gambling paraphernalia, competent evidence against the accused? We think there was no violation of the constitutional guaranty of privilege from unlawful search or seizure in the admission of this testimony. Nor do we think the accused was compelled to incriminate himself. He did not take the witness stand in his *598 own behalf, as was his privilege under the laws of the State of New York. He was not compelled to testify concerning the papers or make any admission about them.

The origin of these amendments is elaborately considered in Mr. Justice Bradley's opinion in the Boyd case, supra. The security intended to be guaranteed by the Fourth Amendment against wrongful search and seizures is designed to prevent violations of private security in person and property and unlawful invasion of the sanctity of the home of the citizen by officers of the law, acting under legislative or judicial sanction, and to give remedy against such usurpations when attempted. But the English and nearly all of the American cases have declined to extend this doctrine to the extent of excluding testimony which has been obtained by such means, if it is otherwise competent. In Boyd's case the law held unconstitutional, virtually compelled the defendant to furnish testimony against himself in a suit to forfeit his estate, and ran counter to both the Fourth and Fifth Amendments. The right to issue a search warrant to discover stolen property or the means of committing crimes, is too long established to require discussion. The right of seizure of lottery tickets and gambling devices, such as policy slips, under such warrants, requires no argument to sustain it at this day. But the contention is that, if in the search for the instruments of crime, other papers are taken, the same may not be given in evidence. As an illustration, if a search warrant is issued for stolen property and burglars' tools be discovered and seized, they are to be excluded from testimony by force of these amendments. We think they were never intended to have that effect, but are rather designed to protect against compulsory testimony from a defendant against himself in a criminal trial, and to punish wrongful invasion of the home of the citizen or the unwarranted seizure of his papers and property, and to render invalid legislation or judicial procedure having such effect.

It is further urged that the law of the State of New York, Penal Code, § 344b, which makes the possession by persons other than a public officer of papers or documents, being the record of chances or slips in what is commonly known as *599 policy, or policy slips, or the possession of any paper, print or writing commonly used in playing or promoting the game of policy, presumption of possession thereof knowingly in violation of section 344a, is a violation of the Fourteenth Amendment to the Constitution of the United States in that it deprives a citizen of his liberty and property without due process of law. We fail to perceive any force in this argument. The policy slips are property of an unusual character and not likely, particularly in large quantities, to be found in the possession of innocent parties. Like other gambling paraphernalia, their possession indicates their use or intended use, and may well raise some inference against their possessor in the absence of explanation. Such is the effect of this statute. Innocent persons would have no trouble in explaining the possession of these tickets, and in any event the possession is only prima facie evidence, and the party is permitted to produce such testimony as will show the truth concerning the possession of the slips. Furthermore, it is within the established power of the State to prescribe the evidence which is to be received in the courts of its own government. Fong Yue Ting v. United States, 149 U.S. 698, 729.

It is argued, lastly, that section 344b, is unconstitutional because the possession of the policy tickets is presumptive evidence against all except public officers, and it is urged that public officials, from the governor to notaries public, would thus be excluded from the terms of the law which apply to all non-official persons. This provision was evidently put into the statute for the purpose of excluding the presumption raised by possession where such tickets or slips are seized and are in the custody of officers of the law. This was the construction given to the act by the New York courts, and is the only one consistent with its purposes. The construction suggested would lead to a manifest absurdity, which has not received, and is not likely to receive, judicial sanction. We find nothing in the record before us to warrant a reversal of the conclusions reached in the New York Court of Appeals, and its

Judgment will be affirmed.
"""

# Extract all information
extracted_info = extract_information(example_text)
print(extracted_info)
