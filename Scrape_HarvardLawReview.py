import requests
from bs4 import BeautifulSoup

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/91.0.4472.124 Safari/537.36'
    }

# Function to setup the soup object
def get_soup(url,headers):
    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()
        return BeautifulSoup(page.text, 'lxml')
    
    except requests.exceptions.HTTPError as e:
        print("HTTP error occurred: ", e)
        return None

def extract_content_HarvardReview(soup):
    title_tag = soup.find('h1', class_='single-article__title')
    content_tag = soup.find('div', class_='entry-content')

    if title_tag and content_tag:
        title = title_tag.text.strip()
        content = content_tag.text.strip()
        return title, content
    else:
        print("Could not find the title or content on the page.")
        return None, None

#save into TXT file format
def save_content(title,content):
    filename = f"{title}.txt".replace(" ", "_").replace(":", "").replace("/", "_")

    try:
        with open(filename, "w", encoding='utf-8') as file:
            file.write(content)

    except IOError as e:
        print(f"Error saving content to {filename}: {e}")


def scrape_harvard_review(url):

    soup = get_soup(url,headers)

    if soup:
        title, content = extract_content_HarvardReview(soup)
        
        if title and content:
            save_content(title, content)

if __name__ == "__main__":
    urls = ["https://harvardlawreview.org/blog/2023/09/reversing-remands-procedural-uncertainty-in-a-presidents-state-criminal-trials/"
    ,"https://harvardlawreview.org/blog/2024/05/civil-suits-by-parents-against-family-policing-agencies/"]
    for url in urls:
        scrape_harvard_review(url)