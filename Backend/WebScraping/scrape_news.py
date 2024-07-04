import requests
from bs4 import BeautifulSoup

def get_news(url="https://www.law360.com/employment"):
    response = requests.get(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                                            AppleWebKit/537.36 (KHTML, like Gecko)\
                                            Chrome/91.0.4472.124 Safari/537.36' })
    
    soup = BeautifulSoup(response.text, 'lxml')

    html_string = "<div>"

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
                
                html_string += r"<div class=\"${classes.newsItem}\">"+f"\
                    <a href='{full_link}' target='_blank'>{title}</a>\
                    <br><p>{description}</p>\
                    <br><br>\
                    </div>"

    html_string += "</div>"

    return html_string


if __name__ == "__main__":
    html_output = get_news()
    print(html_output)