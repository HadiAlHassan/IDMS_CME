import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_reuters_news():
    # Set up Selenium WebDriver with Chrome
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Navigate to Reuters legal news page
    url = 'https://www.reuters.com/legal/'
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)
    
    try:
        # Check and handle GDPR consent screen
        gdpr_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        gdpr_button.click()
        time.sleep(2)
    except:
        print("GDPR consent screen did not appear or was not handled properly")

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    html_string = "<html><ul>"

    for item in soup.find_all('li', class_='story-collection__list-item__j4SQe'):
        headline_tag = item.find('a', class_='media-story-card__heading__eqhp9')
        if headline_tag:
            headline = headline_tag.text.strip()
            link = headline_tag['href']
            full_link = 'https://www.reuters.com' + link  # Ensure the URL is absolute

            img_tag = item.find('img')
            if img_tag:
                img_url = img_tag['src']
            else:
                img_url = ''

            html_string += f"<li><a href='{full_link}' target='_blank'>{headline}</a><br><img src='{img_url}' alt='Image for {headline}' style='max-width:200px;'><br><br></li>"

    html_string += "</ul></html>"

    return html_string

# Example usage
html_result = get_reuters_news()
print(html_result)
