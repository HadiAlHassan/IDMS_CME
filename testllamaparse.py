from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
import os
load_dotenv()

# set up parser
parser = LlamaParse(
    result_type="markdown",  # "markdown" and "text" are available
    api_key=os.getenv('LLAMA_CLOUD_API_KEY')
)

# use SimpleDirectoryReader to parse our file
file_extractor = {".txt": parser}
documents = SimpleDirectoryReader(input_files=['GRAHAM_v._STATE_OF_WEST_VIRGINIA..txt'], file_extractor=file_extractor).load_data()
print(documents)


index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

query = "summarize the following documentm, mentioning all relevant details?"
response = query_engine.query(query)
print(response)


"""from dotenv import load_dotenv
import os
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.cohere import Cohere
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.cohere import CohereEmbedding

load_dotenv()

api_key = os.getenv('LLAMA_CLOUD_API_KEY')

parser = LlamaParse(
    result_type="markdown",  # "markdown" and "text" are available
    api_key=api_key
)

file_extractor = {".txt": parser}

documents = SimpleDirectoryReader(input_files=['GRAHAM_v._STATE_OF_WEST_VIRGINIA..txt'], file_extractor=file_extractor).load_data()



# create an index from the parsed markdown
index = VectorStoreIndex.from_documents(documents)

# create a query engine for the index
query_engine = index.as_query_engine()

# query the engine
query = "Explain to me the contents of the document."
response = query_engine.query(query)
print(response)"""
