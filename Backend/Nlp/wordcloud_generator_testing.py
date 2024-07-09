from .wordcloud_generator import generate_word_cloud_from_text, update_dataset_and_generate_word_cloud
from pathlib import Path
import os

def test_word_cloud(text):
    input_string = text
    base_path = Path(__file__).parent.parent
    print(base_path)
    csv_path = base_path / 'datasets' / 'stopwords_english.csv'
    legal_word_path = base_path / 'datasets' / 'legal_merged_dataset.csv'
    base_path_ouput = Path(__file__).parent.parent.parent
    print(base_path_ouput)
    output_path = base_path_ouput / 'Frontend' / 'public' / 'wordcloud.png'
    output_path2 = base_path_ouput / 'Frontend' / 'public' / 'general_wordcloud.png'
    
    generate_word_cloud_from_text(input_string, csv_path, output_path)
 
    update_dataset_and_generate_word_cloud(input_string,legal_word_path,csv_path,output_path2)
    
