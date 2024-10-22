# from enum import Enum
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import pyperclip  
# import time  
# import pymupdf
# #--------------------------------------------------------------------------------------------#

# class Source(Enum):
#     HarvardLawReview = 1
#     GoogleScholar = 2
#     LegiFrance = 3
#     CourtListener = 4
#     UsSupremeCourt = 5
#     HighCourtOfAustralia = 6
# #--------------------------------------------------------------------------------------------#

# class Scraper:
    
#     def __init__(self):

#         self.source = None

#         self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
#                          AppleWebKit/537.36 (KHTML, like Gecko) \
#                         Chrome/91.0.4472.124 Safari/537.36' }
        
#         self.Url_Mapper = {


#             Source.HarvardLawReview : {

#                 "url" : "https://harvardlawreview.org/",
#                 "method" : self.scrape_harvard_law_review,
#                 "tags": {
#                     "title": {"tag": "h1", "class": "single-article__title"},
#                     "content": {"tag": "div", "class": "entry-content"}
#                 }
#             },

#             Source.GoogleScholar : {

#                 "url" : "https://scholar.google.com/",
#                 "method" :  self.scrape_google_scholar,
#                  "tags": {
#                     "title": {"tag": "h3", "id": "gsl_case_name"},
#                     "content": {"tag": "div", "id": "gs_opinion_wrapper"}
#                 }
#             },


#             Source.LegiFrance : {

#                 "url" : "https://www.legifrance.gouv.fr/",
#                 "method" : self.scrape_LegiFrance,
#                 "tags": {}  
#             },

#             Source.CourtListener : {

#                 "url" : "https://www.courtlistener.com/",
#                 "method" : self.scrape_court_listener,
#                 "tags": {
#                     "title": {"tag": "h1", "class":""}, 
#                     "content": {"tag": "div", "class": "serif-text"}
#                 }
#             },

#             Source.UsSupremeCourt : {

#                 "url" : "https://www.supremecourt.gov/",
#                 "method" : self.scrape_us_supreme_court,
#                 "tags": {}  # Not Needed, They are in PDF Format
#             },

#             Source.HighCourtOfAustralia : {

#                 "url" : "https://www.hcourt.gov.au/",
#                 "method" : self.scrape_high_court_of_australia,
#                 "tags": {}  # Not Needed, They are in PDF Format
#             }

#         }
# #--------------------------------------------------------------------------------------------#
#     def setup_driver(self):
#         driver = webdriver.Chrome()
#         return driver

#     def determine_Source(self,url):

#         for Source, Source_info in self.Url_Mapper.items():

#             if Source_info['url'] in url:
#                 return Source
            
#         return None
    

#     def get_soup(self,url,headers):
#         try:
#             page = requests.get(url, headers=headers)
#             page.raise_for_status()
#             return BeautifulSoup(page.text, 'lxml')
        
#         except requests.exceptions.HTTPError as e:
#             print("HTTP error occurred: ", e)
#             return None

#     def save_content(self,title,content):
#         filename = f"{title}.txt".replace(":", "").replace("/", "_").replace("\n"," ").replace("\r"," ").replace(" ", "_")

#         try:
#             with open(filename, "w", encoding='utf-8') as file:
#                 file.write(content)

#         except IOError as e:
#             print(f"Error saving content to {filename}: {e}")
# #------------------------------------------------------------------------------------#
#     def extract_content_Byclass(self, soup, tags):
#         title_tag = soup.find(tags['title']['tag'], class_=tags['title']['class'])
#         content_tag = soup.find(tags['content']['tag'], class_=tags['content']['class'])

#         if title_tag and content_tag:
#             title = title_tag.text.strip()
#             content = content_tag.text.strip()
#             return title, content
#         else:
#             print("Could not find the title or content on the page.")
#             return None, None

#     def extract_content_Byid(self, soup, tags):
#         title_tag = soup.find(tags['title']['tag'], id=tags['title']['id'])
#         content_tag = soup.find(tags['content']['tag'],id=tags['content']['id'])

#         if title_tag and content_tag:
#             title = title_tag.text.strip()
#             content = content_tag.text.strip()
#             return title, content
#         else:
#             print("Could not find the title or content on the page.")
#             return None, None
# #------------------------------------------------------------------------------------#
#     def scrape_harvard_law_review(self, url):
        
#         soup = self.get_soup(url, headers=self.headers)
#         if soup:
#             tags = self.Url_Mapper[Source.HarvardLawReview]["tags"]
#             title, content = self.extract_content_Byclass(soup, tags)
#             if title and content:
#                 self.save_content(title, content)


#     def scrape_google_scholar(self, url):
#         soup = self.get_soup(url, headers=self.headers)

#         if soup:
#             tags = self.Url_Mapper[Source.GoogleScholar]["tags"]
#             title, content = self.extract_content_Byid(soup, tags)
#             if title and content:
#                 self.save_content(title, content)
    
#     def scrape_court_listener(self, url):
#         soup = self.get_soup(url, headers=self.headers)

#         if soup:
#             tags = self.Url_Mapper[Source.CourtListener]["tags"]
#             title, content = self.extract_content_Byclass(soup, tags)
#             if title and content:
#                 self.save_content(title, content)

#     def scrape_us_supreme_court(self, url):
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#         except Exception as e:
#             print("Error: ", e)
#         else:
#             doc = pymupdf.open(stream=response.content, filetype="pdf")
#             out = open("output.txt", "wb") # create a text output

#             for page in doc: # iterate the document pages
#                 text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
#                 out.write(text) # write text of page
#                 out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
        
#         finally:
#             out.close() # close the output file

#     def scrape_high_court_of_australia(self, url):
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#         except Exception as e:
#             print("Error: ", e)
#         else:
#             doc = pymupdf.open(stream=response.content, filetype="pdf")
#             out = open("output.txt", "wb") # create a text output

#             for page in doc: # iterate the document pages
#                 text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
#                 out.write(text) # write text of page
#                 out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
        
#         finally:
#             out.close() # close the output file

#     def scrape_LegiFrance(self, url):
#         driver = self.setup_driver()

#         try:
#             driver.get(url)
#             wait = WebDriverWait(driver, 10)

#             # Wait until the copy button is visible and click it
#             copy_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div/div[1]/div/div/ul/li[2]/button")))
#             copy_button.click()

#             # Wait for the text to be copied to the clipboard
#             time.sleep(1)
#             copied_text = pyperclip.paste()

#             # Get the title of the document
#             title = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div[2]/h1").text
            
#             self.save_content(title, copied_text)

#         except Exception as e:
#             print(f"An error occurred: {e}")

#         finally:
#             driver.quit()

# #------------------------------------------------------------------------------------#

#     def Scrape(self,url):

#         self.source = self.determine_Source(url)

#         if self.source:
#             return self.Url_Mapper[self.source]['method'](url)
#         else:
#             print("This website is not supported by the scraper.")


# if __name__=="__main__":
#     scrpay = Scraper()
#     url = input()
#     scrpay.Scrape(url)

import time  
from enum import Enum
from WebScraping.ScrapingException import ScrapingException
import requests
import pyperclip  
import pymupdf
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from pymongo import MongoClient
from gridfs import GridFS
from rest_framework.response import Response
from Utils.db import connect_to_gridfs
from api.serializers import DocGeneralInfoSerializer

class DomainSource(Enum):
    HarvardLawReview = 1
    GoogleScholar = 2
    LegiFrance = 3
    CourtListener = 4
    UsSupremeCourt = 5
    HighCourtOfAustralia = 6

class Scraper:
    
    def __init__(self):


        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                         AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/91.0.4472.124 Safari/537.36' }
        
        self.url_mapper = {


            DomainSource.HarvardLawReview : {

                "url" : "https://harvardlawreview.org/",
                "method" : self.__scrape_webpage,
                "tags": {
                    "title": {"tag": "h1", "class": "single-article__title"},
                    "content": {"tag": "div", "class": "entry-content"}
                }
            },

            DomainSource.GoogleScholar : {

                "url" : "https://scholar.google.com/",
                "method" :  self.__scrape_webpage,
                 "tags": {
                    "title": {"tag": "h3", "id": "gsl_case_name"},
                    "content": {"tag": "div", "id": "gs_opinion_wrapper"}
                }
            },


            DomainSource.LegiFrance : {

                "url" : "https://www.legifrance.gouv.fr/",
                "method" : self.__scrape_legifrance,
                "tags": {}  
            },

            DomainSource.CourtListener : {

                "url" : "https://www.courtlistener.com/",
                "method" : self.__scrape_webpage,
                "tags": {
                    "title": {"tag": "h1", "class":""}, 
                    "content": {"tag": "div", "class": "serif-text"}
                }
            },

            DomainSource.UsSupremeCourt : {

                "url" : "https://www.supremecourt.gov/",
                "method" : self.__extract_text_from_pdf,
                "tags": {}  # Not Needed, They are in PDF Format
            },

            DomainSource.HighCourtOfAustralia : {

                "url" : "https://www.hcourt.gov.au/",
                "method" : self.__extract_text_from_pdf,
                "tags": {}  # Not Needed, They are in PDF Format
            }

        }

    def __setup_driver(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        return driver

    def determine_domain_source(self, url):

        for domain_source, source_info in self.url_mapper.items():

            if url.startswith(source_info['url']):
                return domain_source
            
        return None
    
    def __get_soup(self, url, headers):
        try:
            page = requests.get(url, headers=headers)
            page.raise_for_status()
            return BeautifulSoup(page.text, 'lxml')
        
        except requests.exceptions.HTTPError:
            raise ScrapingException("HTTP error occurred while fetching the URL")
        
        except Exception as e:
            raise ScrapingException(f"An error occurred while fetching the URL: {e}")

    def __save_to_mongo(self, title, content, url):
        try:
            fs = connect_to_gridfs()

            filename = f"{title}.txt"
            filtered_filename = filename.replace(":", "").replace("/", "_").replace("\n"," ").replace("\r"," ")

            existing_website = fs.find_one({'filename': filtered_filename})
            if existing_website:
                raise ScrapingException("This content already exists in the database.")
            
            file_id = fs.put(content.encode('utf-8'), filename=filtered_filename)

            serializer = DocGeneralInfoSerializer(data={'source': url , 'title': filtered_filename, 'author': 'Ahmad'})
            if serializer.is_valid():
                serializer.save()
            
            else:
                raise ScrapingException("Error in saving document general info to MongoDB")

        except Exception as e:
            raise ScrapingException(f"An error occurred while saving the content: {e}")

    def __extract_webpage_content(self, soup, tags):
        
        title_tag = soup.find(tags['title']['tag'], class_= tags['title'].get('class'), id = tags['title'].get('id'))
        content_tag = soup.find(tags['content']['tag'], class_ = tags['content'].get('class'), id = tags['content'].get('id'))

        if title_tag and content_tag:
            title = title_tag.text.strip()
            content = content_tag.text.strip()
            return title, content
        else:
            raise ScrapingException("Could not find the title or content on the page.")

    def __scrape_webpage(self, url):

        domain_source = self.determine_domain_source(url)
        soup = self.__get_soup(url, headers=self.headers)

        if soup:
            tags = self.url_mapper[domain_source]["tags"]
            title, content = self.__extract_webpage_content(soup, tags)

            if title and content:
                self.__save_to_mongo(title, content, url)

    def __extract_text_from_pdf(self, url):
        try:

            response = requests.get(url)
            response.raise_for_status()

            doc = pymupdf.open(stream=response.content, filetype="pdf")

            content = ""

            for page in doc:
                content += page.get_text()

            title = url.split('/')[-1]

            self.__save_to_mongo(title, content, url)
                
        except Exception as e:
            raise ScrapingException(f"{e}")
        
    def __scrape_legifrance(self, url):

        driver = self.__setup_driver()

        try:
            driver.get(url)

            wait = WebDriverWait(driver, 10)
            copy_button = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/main/div/div/div[1]/div/div/ul/li[2]/button")))
            copy_button.click()

            time.sleep(1)
            copied_text = pyperclip.paste()

            title = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div/div/div[2]/h1").text
            self.__save_to_mongo(title, copied_text, url)

        except Exception as e:
            raise ScrapingException(f"An error occurred: {e}")
        
        finally:
            driver.quit()


    def scrape(self, url):

        domain_source = self.determine_domain_source(url)

        if domain_source:
            return self.url_mapper[domain_source]['method'](url)
        else:
            raise ScrapingException("This website is not supported by the scraper.")


if __name__=="__main__":
    scrpay = Scraper()
    url = input()
    scrpay.scrape(url)
    