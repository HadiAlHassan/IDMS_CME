# bring in our LLAMA_CLOUD_API_KEY
import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import cohere
load_dotenv()

llama_api_key = os.getenv('LLAMA_CLOUD_API_KEY')
cohere_api_key = os.getenv('COHERE_API_RAG_KEY')

co = cohere.Client(api_key=cohere_api_key)

parser = LlamaParse(
    result_type = "markdown",  # "markdown" and "text" are available
    api_key = llama_api_key
)

file_extractor = {".txt": parser}
documents = SimpleDirectoryReader(input_files=['GRAHAM_v._STATE_OF_WEST_VIRGINIA..txt'], file_extractor=file_extractor).load_data()


co.chat(model="command-r-plus",
  message="Summarize the document, mention all key details",
  documents = documents,
  preamble="You are a RAG component for an intelligent document management system\
    for legal documents, fulfill the clients query regarding the document to best of your ability"
  )

