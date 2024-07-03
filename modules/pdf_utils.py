import PyPDF2
import pdftitle
from transformers import pipeline
import re

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""  # Ensure we handle None if extract_text() fails
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

# Function to summarize a PDF file
def summarize_pdf(pdf_path, max_length=1024, summary_max_length=130, summary_min_length=30):
    text = extract_text_from_pdf(pdf_path)
    return summarize_large_text(text, max_length, summary_max_length, summary_min_length)

# Function to extract metadata from a PDF file
def extract_metadata(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        info = reader.metadata

        # Use pdftitle to extract the title
        try:
            title = pdftitle.get_title_from_file(pdf_path)
        except:
            title = info.title if info.title else "N/A"

        # Extract author if available in metadata or content
        author = info.author if info.author else "N/A"
    
    return {
        "Title": title if title else "N/A",
        "Author": author if author else "N/A"
    }

# Function to extract title and author from the text
def extract_title_and_author(text):
    # Regular expressions to find possible titles and authors
    title_pattern = re.compile(r"(?:Title:|TITLES?:|Document Title:)\s*(.*)", re.IGNORECASE)
    author_pattern = re.compile(r"(?:Author:|BY:|Authors?:)\s*(.*)", re.IGNORECASE)
    
    title_match = title_pattern.search(text)
    author_match = author_pattern.search(text)
    
    title = title_match.group(1).strip() if title_match else "N/A"
    author = author_match.group(1).strip() if author_match else "N/A"

    return title, author

# Function to process a PDF file
def process_pdf(pdf_path):
    # Extract metadata
    metadata = extract_metadata(pdf_path)
    print("Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    # Summarize the PDF
    # summary = summarize_pdf(pdf_path)
    # print("\nSummary:")
    # print(summary)



