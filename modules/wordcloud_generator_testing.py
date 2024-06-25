from wordcloud_generator import generate_word_cloud_from_string
from pathlib import Path
# Testing the function
if __name__ == "__main__":
    input_string = "lol   gaggggggggggg."
    csv_path = Path(__file__).parent.parent / 'Datasets' / 'legal_merged_dataset.csv'
    output_path = 'wordcloud.svg'
    
    output_path = generate_word_cloud_from_string(input_string, csv_path, output_path)
    print(f"Word cloud saved to {output_path}")
