import requests
from bs4 import BeautifulSoup

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

def extract_content_CourtListener(soup):
        
    title = soup.find('h1')
    content= soup.find('div', class_="serif-text")

    if title and content:

        title = title.text.strip()
        content = content.text.strip()

        return title, content
    
    else:
        print("Could not find the title or content on the page.")
        return None, None


#save into TXT file format
def save_content(title,content):
    filename = f"{title}.txt".replace(" ", "_").replace(":", "").replace("/", "_").replace("\n"," ")

    try:
        with open(filename, "w", encoding='utf-8') as file:
            file.write(content)

    except IOError as e:
        print(f"Error saving content to {filename}: {e}")

#----------------Main APIs---------------------------#



def Scrape_CourtListener(url):
    
    soup = get_soup(url,headers=headers)

    if soup:
        title, content = extract_content_CourtListener(soup)
        
        if title and content:
            save_content(title, content)


if __name__ == "__main__":
    #url = r"https://www.courtlistener.com/opinion/97635/graham-v-west-virginia/?q=graham&type=o&order_by=score%20desc&stat_Precedential=on"
    #url = r"https://www.courtlistener.com/opinion/2196810/onti-inc-v-integra-bank/?type=o&q=%2Conty&type=o&order_by=score%20desc&stat_Precedential=on"
    #url = r"https://www.courtlistener.com/opinion/96015/adams-v-new-york/?type=o&q=&type=o&order_by=score%20desc&stat_Precedential=on"
    url = input()
    Scrape_CourtListener(url)

