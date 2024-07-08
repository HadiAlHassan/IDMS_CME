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
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b',  # e.g., April 30, 1994
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b'  # e.g., December 2024
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
        elif re.match(r'(?:january|february|march|april|may|june|july|august|september|october|november|december) \d{4}', date):
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
Introduction
In recent decades, the family policing system has penetrated more deeply into poor communities, removing children and surveilling families at a rate never before seen. Family policing agencies that execute these removals — despite being state actors — face few constraints on their actions: state laws give agencies broad discretion, and agencies are not bound by many of the constitutional limits that apply to criminal police. However, there are some constitutional protections and state law limits that apply to the conduct of family policing agencies. Families, media, and advocates document systemic exertion of state power over parents outside the limits of agency authority, from unlawful removals to warrantless searches to racially discriminatory practices. While there are established routes to sue police officers who abuse their authority, cases against family policing agencies by parents whose rights are violated are rare.

This piece explores some of the civil cases that have been brought by parents against family policing agencies and considers the challenges and potential of such suits. There’s no question that civil suits by parents face significant obstacles, including the lack of applicable protections for parents, qualified immunity laws, and the lack of attorneys able or willing to bring claims. Civil suits certainly cannot “solve” the problems of family policing, nor replace the central role of movement building and political change. But they can and should be part of a multifaceted strategy to contest and abolish family policing. Civil suits by parents against family policing agencies and child abuse reporters can serve as a limited check on agency power, and — perhaps most importantly — can focus media and court attention on the harms of forcible family separation for parents and children. These suits should be led by impacted families and designed in response to their priorities. In sum, while imperfect, civil suits are an underutilized approach that should be considered more often by advocates fighting family policing.

Family Policing Causes Grievous Harm to Children and Parents
Family policing — even when conducted within the confines of the law — is harmful to children and destroys families and communities. It targets Black and brown families, with structurally racialized approaches and discriminatory outcomes. As the “child welfare” system has grown in scope, it has swept in larger numbers of families and children than ever before. Today, in many parts of the country, 53% of Black children will face an investigation by child protective services before the age of eighteen, while only 28% of white children will.

As Joyce McMillan powerfully argues, while the family policing system markets itself as helping children, it instead grievously harms them. A growing body of data documents the lasting physical, mental, and behavioral harm to children who are removed from their parents, even as compared to children in similarly situated households who remain with their parents. For children, removal from their families causes lasting grief, confusion, and isolation. It increases the risk of juvenile and adult criminal behavior, attachment disorders, and early mortality. Compared to staying with the parent, child removal offers no benefit in terms of cognitive outcomes, academic achievement, mental health, or suicide risk.

The damage to parents from family separation is equally grievous. A child protective services (CPS) investigation, and even temporary separation, subjects families to extreme stress and lasting harm. The trauma of family separation causes long-lasting damage and ravages the social fabric of poor communities of color with intergenerational impacts. It aggravates and compounds other struggles facing low-income and Black parents, including poor maternal and newborn health outcomes and high levels of poverty and violence.

Family Policing Court Systems Are Broken
When courts adjudicate child removal cases, they typically do not consider the harm of separating a child from their parents. The court process focuses only on risks or harm the child faces by staying in the home, adjudicating whether it is “contrary to the welfare” to remain in the home or whether there is a sufficient “risk of harm” to the child in the home. The harms caused to a child and their parents by forced separation and those harms inflicted by the foster care system go unaccounted for.

In addition, family policing agencies operate in secrecy. Most states have high confidentiality standards for dependency cases that prohibit any outside parties from viewing proceedings or related documents. Some will issue gag orders to keep parents from speaking publicly about their cases. This secrecy insulates the agencies and courts from outside scrutiny or accountability.

Meanwhile, there is little oversight of agencies from the juvenile and family courts that oversee dependency cases. These courts notoriously act without regard for constitutional or statutory limitations on their cases, viewing the “best interest of the child” as they conceive of it to take precedence over black letter law that may limit agency authority. Agencies routinely operate outside the law: lying to parents about their ability to decline to speak with the agency, requiring them to sign often blank releases of information that are voluntary, coercing them into signing “safety plans” that remove their children without a court hearing and conducting searches without a warrant. 

While the routine operation of family policing systems is deeply harmful and disturbing, part of what is so concerning is the way that family policing agencies operate with impunity, with few checks on their authority. The juvenile and family courts in which these agencies operate are notorious for giving agencies wide leeway, being outcome driven, and interpreting legal rules and standards to permit egregious agency actions. Moreover, and perhaps most critically, the violence of family separation is normalized in these courts. This makes the judicial actors inured to the consequences of agency actions that may be extralegal and result in family separations. These courts are blind to the grievous injuries caused by the system they propel, and therefore unable to recognize and curtail questionable agency actions.

Civil Cases By Parents Against Family Policing Agencies
Civil suits against criminal police for violations of constitutional rights are relatively common, while civil suits against family policing agencies are still few and far between. Data on these suits is hard to come by; unless the case is reported in the media or publicized by advocates, it is difficult to find. This section describes some recent known cases against family policing agencies and discusses the limitations and challenges surrounding these suits, as well as their potential.

It should be noted here that civil suits against family policing agencies by children subject to family policing systems are far more developed than those by parents. For decades, children’s rights advocates have used impact litigation as a tool to seek to redress harms suffered by children under the care of those agencies. The relationship between agencies and foster children –– that of a guardian with affirmative duties –– along with the fully dependent and “blameless” positionality of the children placed in these systems, has made civil suits by children and children’s rights advocates a viable strategic tool in effecting change. Even so, probably the most important contribution of these suits is bringing the wrongdoing of agencies, and its harmful consequences, into the media and public eye. Many such cases have essentially shamed agencies into settling or changing policies under public pressure, even when the blackletter legal case may have been relatively weak.

There have also been cases by parents against non-agency actors involved in separating their families. Most notably, the family of Beata Kowalski, who committed suicide after being falsely accused of child abuse and separated from her daughter by CPS, won a $261 million award against the hospital where she was initially accused of abuse and whose providers initiated the child protective services reports that resulted in Kowalski’s nightmare of family separation.

Finally, the dichotomy between the interests of parents and children in the family policing context is often a false one: children are just as harmed — or more — by removal from their parents as the parents are. While the fundamental right of parents to parent their children has been articulated in federal constitutional law over time, the right of children to be with their parents and have the love and care of their parents is just as dear. In other words, many cases that have and could be brought by parents against family policing systems can be brought by children too, as the interests of parents and children in staying together and avoiding separation are often aligned.

Existing Civil Suits By Parents Against Family Policing Agencies
a) Challenging Racial Discrimination and State Law Violations
In a recent case in New York City, mother Chanetto Rivers sued the Administration for Children’s Services (ACS) and received a first-of-its-kind $75,000 settlement after her newborn baby was removed solely for marijuana use. New York legalized marijuana in 2021, and the law also indicated that marijuana use alone was not grounds for removing a child. Prior to going into labor, Ms. Rivers smoked marijuana at a family cookout. While giving birth, Ms. Rivers was asked by hospital staff whether she had smoked or had alcohol. When she responded that she had smoked marijuana, the hospital proceeded to test her for drugs without her knowledge or consent. The hospital then tested the baby after birth without Ms. Rivers’ consent. The tests came back positive for marijuana and the hospital called ACS. According to the complaint, ACS instructed the hospital not to discharge the baby to Ms. Rivers, even when the infant was medically cleared for discharge. It took Ms. Rivers a week to recover her baby, and, even after a judge ordered the baby returned to her care, she was subjected to invasive and ongoing scrutiny and onerous requirements by ACS.

Ms. Rivers filed suit in federal district court. The suit named as defendants the City of New York, the Commissioner of ACS, the ACS worker on the case, and the worker’s ACS supervisor. The complaint alleged that the agency had violated New York’s recent law stating that marijuana alone could not be the basis to remove a child from the parent. In doing so, ACS had violated Rivers’ federal and state due process rights.

The complaint also alleged, under Section 1983, that the removal of Ms. Rivers’ baby was part of a race-based pattern and practice by the agency to target and harm Black families in the city, in violation of the Fourteenth Amendment, as well as the state constitution. The complaint emphasized that ACS leadership was made aware of the illegal removal early on and took no action to stop it and that ACS continued to prosecute and terrorize Ms. Rivers with middle-of-the-night pop-up visits, mandatory random drug tests, and intensive requirements for “services” to retain custody of her baby. Among other harms, the complaint indicated that “Ms. Rivers suffered fear, trauma, distress, humiliation, pain and suffering, terror, and mental anguish due to her separation from her infant son within his first week of life,” and that “Ms. Rivers and [her baby] missed crucial moments of bonding, feeding, and skin-to-skin contact.”

Ms. Rivers’ suit further alleges that ACS removed Ms. Rivers’ baby because Ms. Rivers is Black. In building the case for targeted racial discrimination, the complaint heavily emphasizes the long-documented history of racial disparities in ACS removals, ACS’s failure to take action to rectify those disparities despite internal recommendations for steps that could do so, as well as an internal audit of racial bias in ACS. The 2020 internal audit was commissioned in acknowledgment of ACS’s legacy of racially disparate impacts. It included interviews with ACS staff and leadership. According to the complaint, the report from the internal audit concluded that ACS was “a predatory system that specifically targets Black and Brown parents and applies a different level of scrutiny to them throughout their engagement with ACS.” ACS staff reported to auditors feeling pressure “to be more punitive toward Black parents” than white ones and acting to remove children based on fear of retribution from leadership at ACS rather than concerns about children’s safety. The report was not published or made public by ACS; advocates only obtained the report through Freedom of Information Law Requests. The complaint alleges that ACS’s actions constituted a “policy and custom of racial discrimination” in violation of the Fourteenth Amendment and state constitutional protections that resulted in the removal of Ms. Rivers’ baby.

In September of 2023, ACS agreed to settle the suit and pay Ms. Rivers $75,000. This settlement was reported as the first of its kind in the wake of the new marijuana law.

Ms. Rivers’ suit illustrates the potential of civil suits by parents to hold agencies accountable to state law and to address racial discrimination in the family policing system. At the very least, this suit brought publicity and media attention to the racist practices of ACS, shaming the agency into a settlement. At most, it may have protected parents in the future from removals based solely on marijuana use.

b) Challenging Warrantless Searches in Violation of the Fourth Amendment
Several suits by parents are challenging the child protective service agencies’ common practice of entering homes without a warrant. A recent analysis found that “[e]ach year, child protective services agencies inspect the homes of roughly 3.5 million children, opening refrigerators and closets without a warrant. Only about 5% of these kids are ultimately found to have been physically or sexually abused.” In a landmark class-action case filed in February 2024, parents in New York City sued for the tens of thousands of warrantless searches that take place annually by New York’s Administration for Children’s Services (ACS).  

The class action alleges that, in violation of the Fourth Amendment, ACS uses coercive tactics—such as lying to parents about their rights, threatening to call the police, or threatening to take their children away — to force their way into parents’ homes. ACS does not seek court orders to permit the searches, does not justify the searches via exigent circumstances, nor does it obtain voluntary consent for the searches. The complaint notes that more than 80% of the parents and children subjected to ACS investigation are Black or Hispanic.

The New York class action follows on the heels of several other cases alleging Fourth Amendment violations by family policing agencies against parents. For instance, a mother in New York who faced repeat warrantless searches of her home by ACS agents accompanied by police over the course of three years, which never showed any abuse or neglect on her part, sued alleging violations of her Fourth Amendment rights.  In Massachusetts, parents Josh Sabey and Sarah Perkins filed suit after their two children were forcibly removed from their home in the middle of the night. They allege their Fourth Amendment rights were violated by the removal absent a warrant to search and seize their children. They also allege there were no reasonable grounds for finding there was an imminent danger to their children remaining in their care. The parents were separated from their children for four months before being cleared of any wrongdoing.

The Fourth Amendment challenges by parents raise novel questions about how, if at all, Fourth Amendment protections apply in the family policing context. In a recent analysis of the issue, Professor Tarek Ismail finds that most federal circuits ruling on the issue have found that “CPS agents must obtain a warrant to enter a home during a CPS investigation in the absence of exigency or consent.” However, two circuits have held that family policing agencies do not require a warrant to conduct home searches. He notes that, because the exclusionary rule does not apply in the child protective services context, the issue litigated is not admissibility of evidence but often whether agents who acted are covered by qualified immunity. Ismail persuasively argues that “based on CPS’s broad statutory authority to investigate and the carceral consequences flowing from their searches, courts should apply the same Fourth Amendment restrictions to CPS investigations that would otherwise apply to law enforcement engaged in similar investigative conduct.” The above cases could help pave the way for such protections to be applied.

c) Challenging Child Abuse Registries
In most states, an administrative finding of abuse or neglect, made internally by a family policing agency, can land parents on a child abuse registry. These registries are routinely searched when parents then seek employment in areas that include interaction with children or in law enforcement, if they seek to care for a child who is not their own, or when applying for licensure for certain professions. Parents have almost no opportunity to contest their inclusion on such a registry and remain on the registry even if they are cleared of abuse or neglect in an adjacent court proceeding.

In 2022, parents in Pennsylvania sued the family policing agency, alleging that inclusion on such registries without due process was unconstitutional. The case challenged “the unconstitutionally flawed process of immediately placing individuals on the ChildLine registry based solely on indicated reports without first providing the individual with prior notice and a hearing prior to being placed on the registry.” In email correspondence, counsel on the case confirmed that the case remains pending before the Commonwealth Court of Pennsylvania.

Child abuse registries were successfully challenged by a New York parent in the nineties in  Valmonte v. Bane, in which the Second Circuit ruled that such registries do implicate a liberty interest and require certain procedures to ensure due process. The court found that New York’s child abuse registry did not meet due process standards, as local child protective agencies had only to find that there was “some credible evidence” to support a report of abuse or neglect to mark it as “indicated” and place the accused parent on the registry.

Civil challenges by parents to child abuse registries, if successful, have the potential to stop the broad and lasting impact of inclusion in such registries on individual parents, as well as to limit the broad impact these registries have on communities of color who are targeted by family policing agencies. By publicizing the harm these registries can cause, such suits may help support legislative changes to contain or eradicate such registries.

d) Challenging Removals from Victims of Domestic Violence
While not as recent, one of the landmark victories brought by parents (and their children) against a family policing agency was Nicholson v. Scoppetta, a class action case by parents who were victims of domestic violence and whose children were removed for that reason. The case challenged New York’s family policing agency’s policy of removing children from mothers who had been the victims of domestic abuse, where the mothers had not engaged in any violence themselves, for failure to prevent the child from witnessing domestic violence. The court found that the statutory definition of “neglect” did not encompass circumstances only where a parent was the victim of domestic abuse, and the child was exposed to that violence. To constitute neglect, there must be an additional showing:

that a child’s physical, mental or emotional condition has been impaired or is in imminent danger of becoming impaired and second, that the actual or threatened harm to the child is a consequence of the failure of the parent or caretaker to exercise a minimum degree of care in providing the child with proper supervision or guardianship.

Nicholson is an example of how advocates can attack state laws that are overbroad and grant juvenile and family courts seemingly unfettered discretion. By amassing a class of plaintiffs all similarly harmed by this interpretation, and articulating the harm they faced outside of the usual courts in which such cases were processed, this case succeeded in setting a clear limit on the authority of family policing agencies.

Limitations, Challenges, and Potential of Civil Suits
Unlike traditional policing, family policing agencies are not bound by criminal constitutional protections. They are not normally required to advise families of their rights, there is no right to remain silent, no public jury trial, and no right to face one’s accuser. The lack of constitutional protections limits what lawsuits can be brought alleging that the state has violated a parent’s constitutional rights because those rights simply are not guaranteed in the family policing context. That said, such protections could be defined and brought about through challenges that highlight the violations of people’s rights that occur through family policing.

In addition, agency actions are shrouded in secrecy, making it hard to get information and expose their indiscretions. The strict confidentiality provisions are designed to protect the privacy interests of all parties involved, including the minor children. However, these provisions also give cover to agency actions, make it hard to expose agency wrongdoing, and keep outrageous prosecutions of parents out of the public eye. This makes it hard to identify and bring cases but also means that civil litigation can be particularly important in exposing the egregious practices that occur under cover.

Moreover, broad, vague, ill-defined legal standards give enormous leeway to agencies and juvenile or family courts to unjustly investigate and remove children from parents with little cause. As a result of these standards, much of the harm caused by agencies and courts is considered within the broad brush of the law. Still, civil cases may have the potential to tighten those standards (as in Nicholson) or to publicly shame agencies into adopting better protocols.

Finally, there are few attorneys prepared to bring cases. In some part, it is likely because the outcome is too uncertain, and therefore payment uncertain, to justify bringing a suit. With so few prior cases on which to gauge the viability of such a case, and the dollar value of a successful case, attorneys are likely hesitant to pursue them. It may also be because of the taint or stigma associated with parents who are accused of abuse or neglect. This stigma may mean some attorneys and public interest legal entities are reticent to fight on behalf of this client base.

As David Lansner, one of the few attorneys who brings civil cases on behalf of parents has reported, parents cannot succeed in suing if they don’t first get their kids back. In an interview with Rise Magazine, he stated that “[i]f you don’t get your kids back, it doesn’t matter that they violated your procedural rights. You’re not going to win. And the city will try to never return your kids.” In other words, many of the parents whose rights are violated can never challenge those violations because without custody over their children, judges and juries are incredibly skeptical of parents claiming prosecutorial abuse or agency neglect. This means that the families that are suing to enforce stricter standards on the system are likely not its primary victims.

Conclusion
While there are limitations and challenges to bringing civil suits against family policing agencies and child abuse reporters, these suits offer some potential to check agencies, bring much-needed attention to the harms of family policing and separation, and get justice for individual families who have been harmed by separation. Led by impacted parents and with their goals at the center of all efforts, attorneys, and advocates should continue to explore routes for bringing civil suits against agencies on behalf of parents as part of a strategy to check and combat the actions of family policing agencies. Such cases can complement the central work of movement organizing and building political pressure to eliminate family policing.
"""

# Extract all information
extracted_info = extract_information(example_text)
print(extracted_info)
