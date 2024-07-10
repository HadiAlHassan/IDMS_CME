from .wordcloud_generator import generate_word_cloud_from_text, update_dataset_and_generate_word_cloud
from pathlib import Path
 
def test_word_cloud(text):
    csv_path = Path(__file__).parent.parent / 'datasets' / 'stopwords_english.csv'
    dataset_path = Path(__file__).parent.parent / 'datasets' / 'legal_merged_dataset.csv'
    output_path = Path(__file__).parent.parent.parent / 'Frontend' / 'public' / 'wordcloud.png'
    output_path2 = Path(__file__).parent.parent.parent / 'Frontend' / 'public' / 'general_wordcloud.png'
   
    generate_word_cloud_from_text(text, csv_path, output_path)
    print(f"Word cloud saved to {output_path}")
 
    update_dataset_and_generate_word_cloud(text, dataset_path, csv_path, output_path2)
    print(f"Word cloud saved to {output_path2}")