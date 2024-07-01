from transformers import pipeline

# Function to read text from a TXT file
def extract_text_from_txt(file):
    text = file.read()  # Read the content from the file object
    return text

# Function to split text into chunks
def split_text(text, max_length=1024):
    words = text.split()  # Split text into words
    chunks = []
    chunk = []

    for word in words:
        # Add word to current chunk and check length
        chunk.append(word)
        if len(' '.join(chunk)) > max_length:
            # If length exceeds max_length, save the current chunk and start a new one
            chunks.append(' '.join(chunk[:-1]))
            chunk = [word]
    
    # Append the last chunk
    if chunk:
        chunks.append(' '.join(chunk))
    
    return chunks

# Initialize the BART summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to summarize large text by splitting it into chunks
def summarize_large_text(text, max_length=1024, summary_max_length=130, summary_min_length=30):
    chunks = split_text(text, max_length)
    summaries = [summarizer(chunk, max_length=summary_max_length, min_length=summary_min_length, do_sample=False) for chunk in chunks]
    # Combine summaries
    combined_summary = " ".join([summary[0]['summary_text'] for summary in summaries])
    return combined_summary

# Function to summarize a TXT file
def summarize_txt(file, max_length=1024, summary_max_length=130, summary_min_length=30):
    text = extract_text_from_txt(file)
    return summarize_large_text(text, max_length, summary_max_length, summary_min_length)

# Main function to process a TXT file
def process_txt(file):
    # Summarize the TXT file
    summary = summarize_txt(file)
    print("\nSummary:")
    print(summary)

# # Example usage
# txt_file_path = 'pdfs/Reversing_Remands_Procedural_Uncertainty_in_a_President’s_State_Criminal_Trials.txt'  # Replace with your actual TXT file path

# # Open the file and process it
# with open(txt_file_path, 'r', encoding='utf-8') as file:
#     process_txt(file)
