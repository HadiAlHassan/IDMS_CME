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

def extract_content_googleScholar(soup):
    title_tag = soup.find('h3', id="gsl_case_name")

    content_tag = soup.find('div', id='gs_opinion_wrapper')

    if title_tag and content_tag:
        title = title_tag.text.strip()
        content = content_tag.text.strip()
        return title, content
    else:
        print("Could not find the title or content on the page.")
        return None, None

#save into TXT file format
def save_content(title,content):
    filename = f"{title}.txt".replace(" ", "_").replace(":", "").replace("/", "_").replace("\n"," ").replace("\r"," ")

    try:
        with open(filename, "w", encoding='utf-8') as file:
            file.write(content)

    except IOError as e:
        print(f"Error saving content to {filename}: {e}")


def get_doc_scholar(url):
    soup = get_soup(url,headers=headers)

    if soup:
        title, content = extract_content_googleScholar(soup)

        if title and content:
            save_content(title, content)

if __name__ == "__main__":
    #url = "https://scholar.google.com/scholar_case?case=913703117340005992&q=state&hl=en&as_sdt=2006"
    url= input()
    get_doc_scholar(url)