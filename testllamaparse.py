import os
import time
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.llms.cohere import Cohere
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.cohere.base import CohereEmbedding
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.indices.prompt_helper import PromptHelper


load_dotenv()

llama_cloud_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")

parsing_prompt = "You are a legal document parses for an intelligent document management system.\
                Extract all relevant details from the document, in anticipation of a search query related to any detail."

parser = LlamaParse(
    result_type = "markdown",  
    api_key = llama_cloud_api_key,
    parsing_instruction = parsing_prompt
)
 
# use SimpleDirectoryReader to parse our file
file_extractor = {".txt": parser}

parse_begin = time.time()
documents = SimpleDirectoryReader(input_files=['BELL_ATLANTIC_CORPORATION_et_al.,_Petitioners,__v.__William_TWOMBLY_et_al..txt'], file_extractor = file_extractor).load_data()
parse_duration = time.time() - parse_begin

#Setting the embedding and feeding to the index
embed_model = CohereEmbedding(
    api_key = cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_document",
    embedding_type="binary",
)

index = VectorStoreIndex.from_documents(
    documents=documents, embed_model=embed_model
)

embed_model = CohereEmbedding(
    api_key=cohere_api_key,
    model_name="embed-english-v3.0",
    input_type="search_query",
    embedding_type="float",
)

#Chunk size
Settings.llm = Cohere(api_key = cohere_api_key, model="command-r")
Settings.embed_model = embed_model

prompt_helper = PromptHelper(
    context_window=2048,  # set this to the model's maximum context size
    num_output=512,  # set this to the desired output size
    chunk_overlap_ratio=0.1,  # set this based on your preference
    chunk_size_limit=512  # set this based on your preference
 )

Settings.prompt_helper = prompt_helper

# Create a cohere reranker
cohere_rerank = CohereRerank(api_key= cohere_api_key)

# Create the query engine
query_engine = index.as_query_engine(node_postprocessors=[cohere_rerank])




# Generate the response
start_time = time.time()
response = query_engine.query("Explain to me the details of the case",)
response_time = time.time() - start_time

print(response)

print(f"Parse duration: {parse_duration}\n \
        Query duration: {response_time}")


