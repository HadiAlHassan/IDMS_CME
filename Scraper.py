from enum import Enum
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip  
import time  
import pymupdf
#--------------------------------------------------------------------------------------------#
class Source(Enum):
    HarvardLawReview = 1
    GoogleScholar = 2
    LegiFrance = 3
    CourtListener = 4
    UsSupremeCourt = 5
    HighCourtOfAustralia = 6
#--------------------------------------------------------------------------------------------#

class Scraper:
    
    def __init__(self):

        self.source = None

        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                         AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/91.0.4472.124 Safari/537.36' }
        
        self.Url_Mapper = {


            Source.HarvardLawReview : {

                "url" : "https://harvardlawreview.org/",
                "method" : self.scrape_harvard_law_review,
                "tags": {
                    "title": {"tag": "h1", "class": "single-article__title"},
                    "content": {"tag": "div", "class": "entry-content"}
                }
            },

            Source.GoogleScholar : {

                "url" : "https://scholar.google.com/",
                "method" :  self.scrape_google_scholar,
                 "tags": {
                    "title": {"tag": "h3", "id": "gsl_case_name"},
                    "content": {"tag": "div", "id": "gs_opinion_wrapper"}
                }
            },


            Source.LegiFrance : {

                "url" : "https://www.legifrance.gouv.fr/",
                "method" : self.scrape_LegiFrance,
                "tags": {}  
            },

            Source.CourtListener : {

                "url" : "https://www.courtlistener.com/",
                "method" : self.scrape_court_listener,
                "tags": {
                    "title": {"tag": "h1", "class":""}, 
                    "content": {"tag": "div", "class": "serif-text"}
                }
            },

            Source.UsSupremeCourt : {

                "url" : "https://www.supremecourt.gov/",
                "method" : self.scrape_us_supreme_court,
                "tags": {}  # Not Needed, They are in PDF Format
            },

            Source.HighCourtOfAustralia : {

                "url" : "https://www.hcourt.gov.au/",
                "method" : self.scrape_high_court_of_australia,
                "tags": {}  # Not Needed, They are in PDF Format
            }

        }
#--------------------------------------------------------------------------------------------#
    def setup_driver(self):
        driver = webdriver.Chrome()
        return driver

    def determine_Source(self,url):

        for Source, Source_info in self.Url_Mapper.items():

            if Source_info['url'] in url:
                return Source
            
        return None
    

    def get_soup(self,url,headers):
        try:
            page = requests.get(url, headers=headers)
            page.raise_for_status()
            return BeautifulSoup(page.text, 'lxml')
        
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred: ", e)
            return None

    def save_content(self,title,content):
        filename = f"{title}.txt".replace(":", "").replace("/", "_").replace("\n"," ").replace("\r"," ").replace(" ", "_")

        try:
            with open(filename, "w", encoding='utf-8') as file:
                file.write(content)

        except IOError as e:
            print(f"Error saving content to {filename}: {e}")
#------------------------------------------------------------------------------------#
    def extract_content_Byclass(self, soup, tags):
        title_tag = soup.find(tags['title']['tag'], class_=tags['title']['class'])
        content_tag = soup.find(tags['content']['tag'], class_=tags['content']['class'])

        if title_tag and content_tag:
            title = title_tag.text.strip()
            content = content_tag.text.strip()
            return title, content
        else:
            print("Could not find the title or content on the page.")
            return None, None

    def extract_content_Byid(self, soup, tags):
        title_tag = soup.find(tags['title']['tag'], id=tags['title']['id'])
        content_tag = soup.find(tags['content']['tag'],id=tags['content']['id'])

        if title_tag and content_tag:
            title = title_tag.text.strip()
            content = content_tag.text.strip()
            return title, content
        else:
            print("Could not find the title or content on the page.")
            return None, None
#------------------------------------------------------------------------------------#
    def scrape_harvard_law_review(self, url):
        
        soup = self.get_soup(url, headers=self.headers)
        if soup:
            tags = self.Url_Mapper[Source.HarvardLawReview]["tags"]
            title, content = self.extract_content_Byclass(soup, tags)
            if title and content:
                self.save_content(title, content)


    def scrape_google_scholar(self, url):
        soup = self.get_soup(url, headers=self.headers)

        if soup:
            tags = self.Url_Mapper[Source.GoogleScholar]["tags"]
            title, content = self.extract_content_Byid(soup, tags)
            if title and content:
                self.save_content(title, content)
    
    def scrape_court_listener(self, url):
        soup = self.get_soup(url, headers=self.headers)

        if soup:
            tags = self.Url_Mapper[Source.CourtListener]["tags"]
            title, content = self.extract_content_Byclass(soup, tags)
            if title and content:
                self.save_content(title, content)

    def scrape_us_supreme_court(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print("Error: ", e)
        else:
            doc = pymupdf.open(stream=response.content, filetype="pdf")
            out = open("output.txt", "wb") # create a text output

            for page in doc: # iterate the document pages
                text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
                out.write(text) # write text of page
                out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
        
        finally:
            out.close() # close the output file

    def scrape_high_court_of_australia(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print("Error: ", e)
        else:
            doc = pymupdf.open(stream=response.content, filetype="pdf")
            out = open("output.txt", "wb") # create a text output

            for page in doc: # iterate the document pages
                text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
                out.write(text) # write text of page
                out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
        
        finally:
            out.close() # close the output file

    def scrape_LegiFrance(self, url):
        driver = self.setup_driver()

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
            
            self.save_content(title, copied_text)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()

#------------------------------------------------------------------------------------#

    def Scrape(self,url):

        self.source = self.determine_Source(url)

        if self.source:
            return self.Url_Mapper[self.source]['method'](url)
        else:
            print("This website is not supported by the scraper.")


if __name__=="__main__":
    scrpay = Scraper()
    url = input()
    scrpay.Scrape(url)