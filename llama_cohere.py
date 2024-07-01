import os
from dotenv import load_dotenv
from llama_index.llms.cohere import Cohere
from llama_index.core import VectorStoreIndex

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.cohere import CohereEmbedding



# Get the API key from environment variable
api_key = os.getenv('COHERE_API_RAG_KEY')
resp = Cohere(api_key=api_key,model="command")

# set up parser
parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

embed_model = CohereEmbedding(
    cohere_api_key="{API_KEY}",
    model_name="embed-english-v3.0", # Supports all Cohere embed models
    input_type="search_query", # Required for v3 models
)

# Generate Embeddings
embeddings = embed_model.get_text_embedding("Welcome to Cohere!")

# use SimpleDirectoryReader to parse our file
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(input_files=['GRAHAM_v._STATE_OF_WEST_VIRGINIA..txt'], file_extractor=file_extractor).load_data()
print(documents)

# create an index from the parsed markdown
index = VectorStoreIndex.from_documents(documents)

# create a query engine for the index
query_engine = index.as_query_engine()

# query the engine
query = "Explain to me the contents of the document."
response = query_engine.query(query)
print(response)
