import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip  # Library to access the clipboard
import time  # To handle any necessary delays

def setup_driver():
    driver = webdriver.Chrome()
    return driver

#save into TXT file format
def save_content(title,content):
    filename = f"{title}.txt".replace(" ", "_").replace(":", "").replace("/", "_").replace("\n"," ")

    try:
        with open(filename, "w", encoding='utf-8') as file:
            file.write(content)

    except IOError as e:
        print(f"Error saving content to {filename}: {e}")

def scrape_legifrance(url):
    """Scrapes content from the given LegiFrance URL and saves it to a text file."""
    driver = setup_driver()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Wait until the copy button is visible and click it
        copy_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div/div[1]/div/div/ul/li[2]/button")))
        copy_button.click()

        # Wait for the text to be copied to the clipboard
        time.sleep(1)
        copied_text = pyperclip.paste()

        # Get the title of the document
        title = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div[2]/h1").text
        
        save_content(title, copied_text)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://www.legifrance.gouv.fr/cons/id/CONSTEXT000049631354?init=true&page=1&query=&searchField=ALL&tab_selection=constit"
    scrape_legifrance(url)
