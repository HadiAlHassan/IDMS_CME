# initializations.py
from llama_parse import LlamaParse
from llama_index.embeddings.cohere.base import CohereEmbedding
from chromadb import PersistentClient
from llama_index.core.node_parser import HierarchicalNodeParser, SentenceSplitter
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from dotenv import load_dotenv  
import os

load_dotenv()

# language detection api
language_detection_api_key = os.getenv("DETECT_LANGUAGE_API_KEY")


# Initialize LlamaParse
llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")

parsing_prompt = ("You are a legal document parser for an intelligent document management system. "
                  "Extract all relevant details from the document, in anticipation of a search query related to any detail.")

parser = LlamaParse(
    result_type="markdown",
    api_key=llama_cloud_api_key,
    parsing_instruction=parsing_prompt
)

# Initialize Cohere Embedding
cohere_api_key = os.getenv("COHERE_API_KEY")

embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_document",
    embedding_type="int8",
)

# Initialize ChromaDB client and vector store
db_client = PersistentClient(path="./chroma_db")
chroma_collection = db_client.get_or_create_collection("documents")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Initialize Hierarchical Node Parser
hierarchical_node_parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 1024, 512]
)

# Initialize VectorStoreIndex
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context,
    embed_model=embed_model,
    transformations=[hierarchical_node_parser, SentenceSplitter(chunk_size=1024, chunk_overlap=20)]
)
