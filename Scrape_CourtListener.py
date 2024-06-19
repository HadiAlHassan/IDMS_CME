import requests
from bs4 import BeautifulSoup

def Scrape_CL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    page = requests.get(url, headers=headers)
  

    #check the page status
    if page.status_code != 200:
        raise Exception(f"Failed to load page: {page.status_code}")
        
    soup = BeautifulSoup(page.text, 'lxml')
    content= soup.find('div', class_="serif-text")
    title = soup.find('h1').text
    title = title.replace(":", "").replace("/", "_").replace("\n"," ").replace(","," ").replace("."," ")
    with open(f"{title}.txt", "w", encoding="utf-8") as file:
        file.write(content.text)

if __name__ == "__main__":
    #url = r"https://www.courtlistener.com/opinion/97635/graham-v-west-virginia/?q=graham&type=o&order_by=score%20desc&stat_Precedential=on"
    #url = r"https://www.courtlistener.com/opinion/2196810/onti-inc-v-integra-bank/?type=o&q=%2Conty&type=o&order_by=score%20desc&stat_Precedential=on"
    #url = r"https://www.courtlistener.com/opinion/96015/adams-v-new-york/?type=o&q=&type=o&order_by=score%20desc&stat_Precedential=on"
    url = input()
    Scrape_CL(url)

