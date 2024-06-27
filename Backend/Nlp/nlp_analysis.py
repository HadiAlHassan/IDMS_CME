import PyPDF2
from pathlib import Path
import spacy
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re
import json
from django.core.files.uploadedfile import InMemoryUploadedFile

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_metadata_pdf(file:InMemoryUploadedFile):
    # Read PDF
    text = ""
    file.open()  # Ensure the file is opened in binary mode
    pdf_reader = PyPDF2.PdfReader(file)
    metadata = pdf_reader.metadata
        
    for page in pdf_reader.pages:
        text += page.extract_text()

    document_metadata = {
        'title': metadata.get('/Title', 'No title found'),
        'author': metadata.get('/Author', 'No author found'),
        'summary': summarize_text(text),
        'language': detect_language(text),
        'confidentiality': extract_confidentiality(text),
        'locations': extract_locations(text),
        'references': extract_references(text),
        'in_text_citations': extract_in_text_citations(text),
        'word_count': count_words(text)
    }

    return document_metadata

def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

def detect_language(text):
    return detect(text)

def extract_confidentiality(text):
    # Simple regex-based search for confidentiality terms
    confidentiality_terms = ['confidential', 'proprietary', 'sensitive', 'classified']
    for term in confidentiality_terms:
        if re.search(r'\b' + term + r'\b', text, re.IGNORECASE):
            return True
    return False

def extract_locations(text):
    doc = nlp(text)
    locations = set()
    for ent in doc.ents:
        if ent.label_ == 'GPE':  # GPE = Geopolitical Entity
            locations.add(ent.text)
    return list(locations)

def extract_references(text):
    # Simple regex-based search for references (e.g., URLs, DOIs)
    urls = re.findall(r'(https?://\S+)', text)
    dois = re.findall(r'\b10.\d{4,9}/[-._;()/:A-Z0-9]+\b', text, re.IGNORECASE)
    return {'urls': urls, 'dois': dois}

def extract_in_text_citations(text):
    # Regex to find in-text citations like (Author, Year) or [Number]
    author_year_citations = re.findall(r'\(([^)]+, \d{4})\)', text)
    number_citations = re.findall(r'\[\d+\]', text)
    return {'author_year': author_year_citations, 'number': number_citations}

def count_words(text):
    words = text.split()
    return len(words)

#####################################################################################################################

import spacy
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_metadata_text(text):
    # Extract title using regex
    title_match = re.search(r'([^\n\r]+)', text.strip())
    title = title_match.group(0).strip() if title_match else 'No title found'

    # Extract author using regex
    author_match = re.search(r'Author: ([^\n\r]+)', text)
    author = author_match.group(1).strip() if author_match else 'No author found'

    document_metadata = {
        'title': title,
        'author': author,
        'summary': summarize_text(text),
        'language': detect_language(text),
        'confidentiality': extract_confidentiality(text),
        'locations': extract_locations(text),
        'references': extract_references(text),
        'in_text_citations': extract_in_text_citations(text),
        'word_count': count_words(text)
    }

    return document_metadata

def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

def detect_language(text):
    return detect(text)

def extract_confidentiality(text):
    # Simple regex-based search for confidentiality terms
    confidentiality_terms = ['confidential', 'proprietary', 'sensitive', 'classified']
    for term in confidentiality_terms:
        if re.search(r'\b' + term + r'\b', text, re.IGNORECASE):
            return True
    return False

def extract_locations(text):
    doc = nlp(text)
    locations = set()
    for ent in doc.ents:
        if ent.label_ == 'GPE':  # GPE = Geopolitical Entity
            locations.add(ent.text)
    return list(locations)

def extract_references(text):
    # Simple regex-based search for references (e.g., URLs, DOIs)
    urls = re.findall(r'(https?://\S+)', text)
    dois = re.findall(r'\b10.\d{4,9}/[-._;()/:A-Z0-9]+\b', text, re.IGNORECASE)
    return {'urls': urls, 'dois': dois}

def extract_in_text_citations(text):
    # Regex to find in-text citations like (Author, Year) or [Number]
    author_year_citations = re.findall(r'\(([^)]+, \d{4})\)', text)
    number_citations = re.findall(r'\[\d+\]', text)
    return {'author_year': author_year_citations, 'number': number_citations}

def count_words(text):
    words = text.split()
    return len(words)
