import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.embeddings.cohere.base import CohereEmbedding
load_dotenv()

llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")


parser = LlamaParse(
    result_type = "markdown",  
    api_key = llama_cloud_api_key
)

# use SimpleDirectoryReader to parse our file
file_extractor = {".txt": parser}
documents = SimpleDirectoryReader(input_files=['GRAHAM_v._STATE_OF_WEST_VIRGINIA..txt'], file_extractor = file_extractor).load_data()
print(documents[0].text)

"""
embeder = CohereEmbedding(api_key = cohere_api_key)

document_embedding = embeder.get_text_embedding(documents[0].text)
"""