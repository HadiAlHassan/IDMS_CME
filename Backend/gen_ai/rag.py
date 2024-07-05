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

llama_cloud_api_key = "llx-R8ls8nAvxmelKcuHKjjMPChplUue9WxRI7y41iq5eVgSP9tD"
cohere_api_key = "5KI2hpHsWl3Zz8LloXDBkeHSoPdduH1j50SvCneU"


@timing_decorator
@api_view(['post'])
def rag(request):
    # initialize client, setting path to save data
    db = chromadb.PersistentClient(path="chroma_db")

    # create collection
    chroma_collection = db.get_or_create_collection("documents")

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    #Setting the embedding and feeding to the index
    embed_model = CohereEmbedding(
        api_key = cohere_api_key,
        model_name = "embed-english-v3.0",
        input_type = "search_document",
        embedding_type = "int8",
    )

    hierarchical_node_parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=[2048, 1024, 512]
    )

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context,
        embed_model=embed_model, 
        transformations=[hierarchical_node_parser, SentenceSplitter(chunk_size=1024, chunk_overlap=20)]
    )

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