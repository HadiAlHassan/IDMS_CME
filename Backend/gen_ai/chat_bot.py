from rest_framework.response import Response
from rest_framework.decorators import api_view
import cohere
import os
import dotenv

from Utils.decorators import timing_decorator

dotenv.load_dotenv()

co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
preamble="You are a legal aid Generative AI tool for an intelligent document management system.\
        Our clients will ask you questions regarding the law, try to answer to the best of your knowledge.\
        Do not answer non legal questions if the client does not establish relevancy. Keep your answers to the point and elaborate when asked"

chat_history = []
@timing_decorator
@api_view(['POST'])
def chatbot(request):

    global chat_history
    query = request.data.get('query')
    if not query:
        return Response({'error': 'No query provided'}, status=400)
    
    messages = [{'text': message['text'], 'is_user': message['is_user'], 'role': 'user' if message['is_user'] else 'assistant'} for message in chat_history]
    messages.append({'text': f'<Question: {query}>', 'is_user': True, 'role': 'user'})

    stream = co.chat_stream(
        model='command-r-plus',
        preamble=preamble,  
        message= f'{preamble} <Question: {query}>',
        temperature=0.5,
        chat_history=messages,
        prompt_truncation='AUTO',
        connectors=[{"id":"web-search"}]
    )
    response_text = ""
    for event in stream:
        if event.event_type == "text-generation":
            response_text += event.text
    chat_history.append({'text': response_text, 'is_user': False, 'role': 'assistant'})
    return Response({'response': response_text}, status=200)