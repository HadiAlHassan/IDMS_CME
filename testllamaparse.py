from dotenv import load_dotenv
import os
# Bring in dependencies
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv('LLAMA_CLOUD_API_KEY')

# Set up parser with the API key
parser = LlamaParse(
    result_type="markdown",  # "markdown" and "text" are available
    api_key=api_key
)

# Use SimpleDirectoryReader to parse our file
file_extractor = {".txt": parser}

documents = SimpleDirectoryReader(input_files=['GRAHAM_v._STATE_OF_WEST_VIRGINIA..txt'], file_extractor=file_extractor).load_data()

# Print the parsed documents
print(documents)
