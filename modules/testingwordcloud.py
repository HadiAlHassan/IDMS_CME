from wordcloud_generator import generate_word_cloud_from_file
from pathlib import Path

def main():
    # Specify the path to the text file
    file_path = Path(__file__).resolve().parent.parent / 'txtfiles' / 'englishtest.txt'
    
    with open(file_path, 'r', encoding='utf-8') as file:
        # Generate word cloud SVG data
        word_cloud_svg = generate_word_cloud_from_file(file)
    
    # Now you can use word_cloud_svg as needed
    print(word_cloud_svg)  # Example: Print the SVG data

if __name__ == '__main__':
    main()