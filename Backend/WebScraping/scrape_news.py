import requests
from bs4 import BeautifulSoup

def get_news(url="https://www.law360.com/employment"):
    response = requests.get(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                                            AppleWebKit/537.36 (KHTML, like Gecko)\
                                            Chrome/91.0.4472.124 Safari/537.36' })
    
    soup = BeautifulSoup(response.text, 'lxml')

    news_items = []
    
    specific_news = {
        "title": "NYT v. OpenAI: The Times’s About-Face",
        "link": "https://harvardlawreview.org/blog/2024/04/nyt-v-openai-the-timess-about-face/",
        "description": "This article discusses the New York Times' legal battle with OpenAI, focusing on the implications for AI and copyright law."
    }
    news_items.append(specific_news)

    

    # Find the news container
    news_container = soup.find('div', id='news-headlines')
    if news_container:
        # Find all the list items within the container
        headlines = news_container.find_all('li', class_='hnews hentry')
        
        # Extract the first 5 headlines
        for idx, headline in enumerate(headlines[:5]):
            headline_tag = headline.find('h3')
            if headline_tag:
                title = headline_tag.get_text(strip=True)
                link = headline_tag.find('a')['href']
                full_link = 'https://www.law360.com' + link  # Ensure the URL is absolute

                description_tag = headline.find('p', class_='entry-content')
                description = description_tag.get_text(strip=True) if description_tag else ''
                
                news_items.append({
                    "title": title,
                    "link": full_link,
                    "description": description
                })

    return news_items

