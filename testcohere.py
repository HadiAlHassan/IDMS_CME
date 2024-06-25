import cohere 

co = cohere.Client(
  api_key="5KI2hpHsWl3Zz8LloXDBkeHSoPdduH1j50SvCneU", # This is your trial API key
) 

query = input()

stream = co.chat_stream( 
  model='command-r-plus',
  message='<YOUR MESSAGE HERE>',
  temperature=0.3,
  chat_history=[],
  prompt_truncation='AUTO',
  connectors=[{"id":"web-search"}]
) 

for event in stream:
  if event.event_type == "text-generation":
    print(event.text, end='')