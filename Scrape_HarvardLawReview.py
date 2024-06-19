import requests
from bs4 import BeautifulSoup

def scrape_harvard_review(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Page loaded successfully!")
        soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = soup.find('h1', class_='single-article__title')
        content_tag = soup.find('div', class_='entry-content')

        if title_tag and content_tag:
            title = title_tag.text.strip()
            content = content_tag.text.strip()

            # Create a valid filename from the title
            filename = f"{title}.txt".replace(" ", "_").replace(":", "").replace("/", "_")

            with open(filename, "w", encoding='utf-8') as file:
                file.write(content)
            print(f"Content saved to {filename}")
        else:
            print("Could not find the title or content on the page.")
    else:
        print(f"Failed to load the page. Status code: {response.status_code}")

if __name__ == "__main__":
    urls = ["https://harvardlawreview.org/blog/2023/09/reversing-remands-procedural-uncertainty-in-a-presidents-state-criminal-trials/"
    ,"https://harvardlawreview.org/blog/2024/05/civil-suits-by-parents-against-family-policing-agencies/"]
    for url in urls:
        scrape_harvard_review(url)