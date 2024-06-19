import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pyperclip  # Library to access the clipboard
import time  # To handle any necessary delays
from googletrans import Translator


def Scrape_LegiFrance(url):    
    driver = webdriver.Chrome()
    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        
        copy_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div/div[1]/div/div/ul/li[2]/button")))
        
        copy_button.click()
        
       #wait for the text to be copied
        time.sleep(1)  

        copied_text = pyperclip.paste()
        
        title = driver.find_element(By.XPATH,"/html/body/div[1]/div/main/div/div/div[2]/h1").text
        title = title.replace(" ", "_").replace(":", "").replace("/", "_")

        with open(f"{title}.txt", "w", encoding="utf-8") as file:
            file.write(copied_text)
        
        print(f"Text copied and saved to {title}.txt")

    except Exception as e:
        print(f"An error occured: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://www.legifrance.gouv.fr/cons/id/CONSTEXT000049631354?init=true&page=1&query=&searchField=ALL&tab_selection=constit"
    Scrape_LegiFrance(url)

    