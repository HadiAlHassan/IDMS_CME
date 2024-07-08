import PyPDF2
import pdftitle
from transformers import pipeline
from io import BytesIO
 
# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
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
def summarize_pdf(pdf_file, max_length=1024, summary_max_length=130, summary_min_length=30):
    text = extract_text_from_pdf(pdf_file)
    return summarize_large_text(text, max_length, summary_max_length, summary_min_length)
 
# Function to extract metadata from a PDF file and include summary
def extract_metadata(pdf_file, max_length=1024, summary_max_length=130, summary_min_length=30):
    reader = PyPDF2.PdfReader(pdf_file)
    info = reader.metadata
 
    # Use pdftitle to extract the title
    try:
        pdf_file.seek(0)  # Reset the file pointer to the beginning
        title = pdftitle.get_title_from_io(pdf_file)
    except:
        title = info.title if info.title else "N/A"
 
    # Extract and summarize the text
    text = extract_text_from_pdf(pdf_file)
    summary = summarize_large_text(text, max_length, summary_max_length, summary_min_length)
 
    metadata = {
        "title": title if title else "No title found",
        "author": info.author if info.author else "No author found",
        "summary": summary
    }
   
    return metadata
 
