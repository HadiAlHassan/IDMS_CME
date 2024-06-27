import PyPDF2
from pathlib import Path

def extract_metadata_pdf(file_path):
    """
    Extract metadata from a PDF file.

    Args:
        file_path (str or Path): Path to the PDF file.

    Returns:
        dict: Metadata extracted from the PDF.
    """
    metadata = {}
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        metadata['num_pages'] = len(pdf_reader.pages)
        metadata['metadata'] = pdf_reader.metadata
    return metadata

# Example usage
file_name = "people-v-hall-sample-case-brief-pdf.pdf"
file_path = Path("C:/Users/LuidovicZgheib.INTERN27-PC/Desktop/Project_Clone/pdfs") / file_name

metadata = extract_metadata_pdf(file_path)
print(metadata)
