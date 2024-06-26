import cohere 
import os
import dotenv

dotenv.load_dotenv()

co = cohere.Client(
  api_key=os.getenv("COHERE_API_KEY"), # This is your trial API key
) 

while (query := input()) != "f101":

  stream = co.chat_stream( 
    model='command-r-plus',
    preamble="You are a legal aid Generative AI tool for an intelligent document management system.\
      Our clients will ask you questions regarding the law, try to answer to the best of your knowledge.\
      Do not answer non legal questions if the client does not establish relevancy. ",
    message= f'<Question: {query}>',
    temperature=0.3,
    chat_history=[],
    prompt_truncation='AUTO',
    connectors=[{"id":"web-search"}]
  ) 

  for event in stream:
    if event.event_type == "text-generation":
      print(event.text, end='')

  print()