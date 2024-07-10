import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import nest_asyncio
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.llms.cohere import Cohere
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.core import SummaryIndex
from llama_index.embeddings.cohere.base import CohereEmbedding
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext, load_index_from_storage
from Utils.decorators import timing_decorator
from  initializations.initializer  import embed_model, index, cohere_api_key



@timing_decorator
@api_view(['post'])
def rag(request):
    #Chunk size
    Settings.llm = Cohere(api_key = cohere_api_key, model="command-r")
    Settings.embed_model = embed_model

    # Create a cohere reranker
    cohere_rerank = CohereRerank(api_key= cohere_api_key)

    # Create the query engine
    query_engine = index.as_query_engine(node_postprocessors=[cohere_rerank])
    
    query = request.data.get('query')

    answer = query_engine.query(query)

    # Ensure the answer is properly serialized
    response_data = {
        'response': answer.__str__()
    }
    return Response(response_data, status=200)