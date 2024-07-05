import pdfplumber
from langdetect import detect
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import textwrap
import time

def extract_text_with_formatting(file):
    """Extract text from a PDF file with formatting using pdfplumber."""
    formatted_text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if text:
                formatted_text += f"Page {page.page_number}\n{text}\n\n"
    return formatted_text

def detect_language(text):
    """Detect the language of the provided text."""
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

def translate_text_in_chunks(text, src_lang, chunk_size=2000, max_attempts=3):
    """Translate text in smaller chunks and return translated chunks as a list."""
    translator = Translator()
    translated_chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        print(f"Translating chunk starting at index {i}, length {len(chunk)}")

        attempt = 0
        while attempt < max_attempts:
            try:
                translated_chunk = translator.translate(chunk, src=src_lang, dest='en').text
                translated_chunks.append(translated_chunk)
                print(f"Successfully translated chunk starting at index {i}")
                break
            except Exception as e:
                print(f"Translation error for chunk starting at index {i}: {e}")
                attempt += 1
                time.sleep(5)

        if attempt == max_attempts:
            translated_chunks.append(f"Translation failed for chunk starting at index {i}.")
            print(f"Translation failed for chunk starting at index {i} after {max_attempts} attempts.")

    return translated_chunks

def save_text_to_pdf(text_chunks, output_path):
    """Save the translated text chunks to a PDF file with formatting."""
    buffer = io.BytesIO()
    can = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    text_object = can.beginText(40, height - 40)
    text_object.setFont("Helvetica", 12)

    for chunk in text_chunks:
        wrapped_text = textwrap.fill(chunk, width=90)
        
        for line in wrapped_text.split('\n'):
            text_object.textLine(line)
            if text_object.getY() < 40:
                can.drawText(text_object)
                can.showPage()
                text_object = can.beginText(40, height - 40)
                text_object.setFont("Helvetica", 12)
        
        can.drawText(text_object)
        can.showPage()

    can.save()

    buffer.seek(0)
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())

def process_pdf(file):
    """Process the PDF file: extract text, detect language, translate, and save to a new PDF."""
    text = extract_text_with_formatting(file)
    if not text:
        print("No text extracted from PDF.")
        return

    print("Extracted Text Preview:\n", text[:1000])

    language = detect_language(text)
    if not language:
        print("Language detection failed.")
        return

    print(f"Detected Language: {language}")

    translated_chunks = translate_text_in_chunks(text, language)
    if translated_chunks:
        print("Translated Text Preview:\n", ''.join(translated_chunks)[:1000])
        save_text_to_pdf(translated_chunks, 'translated_document.pdf')
    else:
        print("Translation failed.")

# Example usage
if __name__ == '__main__':
    # Replace with the path to your PDF document or use an open file object
    with open('pdfs/Chinese_(simplified)_PDF.pdf', 'rb') as pdf_file:  # Example of using a file-like object
        process_pdf(pdf_file)
