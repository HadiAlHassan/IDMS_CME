import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import nest_asyncio
import os
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


load_dotenv()

llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")

parsing_prompt = "You are a legal document parses for an intelligent document management system.\
                Extract all relevant details from the document, in anticipation of a search query related to any detail."

parser = LlamaParse(result_type = "markdown",  
    api_key = llama_cloud_api_key,
    parsing_instruction = parsing_prompt
)

# load some documents
file_extractor = {".txt": parser}

#assume we loaded it from the mongodb
documents = SimpleDirectoryReader(input_files=["Civil_Suits_by_Parents_Against_Family_Policing_Agencies.txt"],file_extractor = file_extractor).load_data()

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

index.insert(documents[0])

#Chunk size
Settings.llm = Cohere(api_key = cohere_api_key, model="command-r")
Settings.embed_model = embed_model

# Create a cohere reranker
cohere_rerank = CohereRerank(api_key= cohere_api_key)

# Create the query engine
query_engine = index.as_query_engine(node_postprocessors=[cohere_rerank])

response = query_engine.query("tell me about Civil Suits_by_Parents_Against_Family_Policing_Agencies ",)
print(response)