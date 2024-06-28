from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, BertForTokenClassification
import torch

# Initialize tokenizers and models
ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
ner_tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
ner_model = AutoModelForTokenClassification.from_pretrained(ner_model_name)

# Initialize NER pipeline
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

def extract_entities(text):
    # Perform NER analysis
    ner_results = ner_pipeline(text)
    
    entities = {"Names": set(), "Locations": set(), "Organizations": set()}

    # Process NER results
    current_entity = ""
    current_type = ""
    for entity in ner_results:
        entity_text = entity['word']
        entity_type = entity['entity']
        
        if entity_text.startswith("##"):
            current_entity += entity_text[2:]
        else:
            if current_entity and current_type:
                if current_type == 'B-PER' or current_type == 'I-PER':
                    entities["Names"].add(current_entity)
                elif current_type == 'B-LOC' or current_type == 'I-LOC':
                    entities["Locations"].add(current_entity)
                elif current_type == 'B-ORG' or current_type == 'I-ORG':
                    entities["Organizations"].add(current_entity)
            
            current_entity = entity_text
            current_type = entity_type
    
    # Add the last entity
    if current_entity and current_type:
        if current_type == 'B-PER' or current_type == 'I-PER':
            entities["Names"].add(current_entity)
        elif current_type == 'B-LOC' or current_type == 'I-LOC':
            entities["Locations"].add(current_entity)
        elif current_type == 'B-ORG' or current_type == 'I-ORG':
            entities["Organizations"].add(current_entity)
    
    return entities

# Example usage with a text
example_text = """
As the Celtics players and coaches spent the week celebrating leading up to the parade, Brad Stevens was back at the Auerbach Center, working out dozens of prospects they could select in the draft this week. They have the 30th and 54th picks and are over the second apron, so they have to nail it on draft night to help build a sustainable team over the coming years.

That’s why after an evening of popping champagne bottles, the front office was back in the early afternoon to get ready for the future.

“The day after, as much as we were excited and celebratory and everything else, you’re always thinking about what this means for what’s next,” Stevens said. “I think that’s just maybe the coach in me or maybe that’s just my age.”

Stevens made a stir last year when the Celtics traded down multiple times on draft night to accumulate a bevy of future second-round picks while selecting Jordan Walsh with the 38th pick. That is not necessarily going to be the norm for this franchise, particularly since bigger deals for Payton Pritchard and potentially Sam Hauser mean the Celtics need to draft more players who have a chance at making the rotation while they are still on their rookie-scale contracts.

Their long-term depth at center is dubious, considering Al Horford’s age and Kristaps Porziņģis’ forthcoming ankle surgery, expected to happen in the next few weeks.

“Kristaps is still in the middle of consulting with some different doctors and specialists, but we anticipate surgery will be soon,” he said.

Because the second apron takes away most of their roster-building tools beyond signing free agents to minimum contracts, getting a center who can develop into a starter down the road most likely would come through the draft. Xavier Tillman and Luke Kornet are both free agents, while Neemias Queta is still under contract, but those players are all far along in their development track.

That’s why Stevens said they made so many trades last season, since they no longer can aggregate salaries in a trade.

“It’ll be interesting to see how it affects the league,” Stevens said. “Are there a lot less trades? That will be interesting to follow and look back and study over the next couple of years. As far as the picks go, if the right person is available at 30, we will take him.”
"""

# Extract entities
entities = extract_entities(example_text)
print(entities)