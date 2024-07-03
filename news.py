import requests
from bs4 import BeautifulSoup

def Fetch_Legal_news(url = "https://www.law360.com/"):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                         AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/91.0.4472.124 Safari/537.36' }
    page = requests.get(url, headers = headers)
    page.raise_for_status()

    soup = BeautifulSoup(page.content, 'lxml')

    news_section = soup.find('div', class_ = 'hidden-md hidden-lg')
    print(news_section.text)



if __name__ == "__main__":
    Fetch_Legal_news()
 