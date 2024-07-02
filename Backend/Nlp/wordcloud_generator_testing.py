from .wordcloud_generator import generate_word_cloud_from_text
from pathlib import Path

def test_word_cloud(text):
    input_string = text
    csv_path = Path(__file__).parent.parent / 'datasets' / 'stopwords_english.csv'
    output_path = Path(__file__).parent.parent.parent / 'Frontend' / 'public' / 'wordcloud.png'
    
    output_path = generate_word_cloud_from_text(input_string, csv_path, output_path)
    print(f"Word cloud saved to {output_path}")