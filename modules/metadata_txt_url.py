# from transformers import pipeline

# # Function to read text from a TXT file
# def extract_text_from_txt(file):
#     text = file.read()  # Read the content from the file object
#     return text

# # Function to split text into chunks
# def split_text(text, max_length=1024):
#     words = text.split()  # Split text into words
#     chunks = []
#     chunk = []

#     for word in words:
#         # Add word to current chunk and check length
#         chunk.append(word)
#         if len(' '.join(chunk)) > max_length:
#             # If length exceeds max_length, save the current chunk and start a new one
#             chunks.append(' '.join(chunk[:-1]))
#             chunk = [word]
    
#     # Append the last chunk
#     if chunk:
#         chunks.append(' '.join(chunk))
    
#     return chunks

# # Initialize the BART summarizer
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# # Function to summarize large text by splitting it into chunks
# def summarize_large_text(text, max_length=1024, summary_max_length=130, summary_min_length=30):
#     chunks = split_text(text, max_length)
#     summaries = [summarizer(chunk, max_length=summary_max_length, min_length=summary_min_length, do_sample=False) for chunk in chunks]
#     # Combine summaries
#     combined_summary = " ".join([summary[0]['summary_text'] for summary in summaries])
#     return combined_summary

# # Function to summarize a TXT file
# def summarize_txt(file, max_length=1024, summary_max_length=130, summary_min_length=30):
#     text = extract_text_from_txt(file)
#     return summarize_large_text(text, max_length, summary_max_length, summary_min_length)

# # Main function to process a TXT file
# def process_txt(file):
#     # Summarize the TXT file
#     summary = summarize_txt(file)
#     print("\nSummary:")
#     print(summary)

# # Example usage
# txt_file_path = 'pdfs/Reversing_Remands_Procedural_Uncertainty_in_a_President’s_State_Criminal_Trials.txt'  # Replace with your actual TXT file path

# # Open the file and process it
# with open(txt_file_path, 'r', encoding='utf-8') as file:
#     process_txt(file)

########HADI'S CODE TWEAK########
# import time  
# from enum import Enum
# import requests
# import pyperclip  
# import pymupdf
# from bs4 import BeautifulSoup


# class DomainSource(Enum):
#     HarvardLawReview = 1
#     GoogleScholar = 2
#     LegiFrance = 3
#     CourtListener = 4
#     UsSupremeCourt = 5
#     HighCourtOfAustralia = 6

# class Scraper:
    
#     def __init__(self):

#         self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
#                          AppleWebKit/537.36 (KHTML, like Gecko) \
#                         Chrome/91.0.4472.124 Safari/537.36' }
        
#         self.url_mapper = {


#             DomainSource.HarvardLawReview : {

#                 "url" : "https://harvardlawreview.org/",
#                 "method" : self.__scrape_webpage,
#                 "tags": {
#                     "title": {"tag": "h1", "class": "single-article__title"},
#                     "content": {"tag": "div", "class": "entry-content"}
#                 }
#             },

#             DomainSource.GoogleScholar : {

#                 "url" : "https://scholar.google.com/",
#                 "method" :  self.__scrape_webpage,
#                  "tags": {
#                     "title": {"tag": "h3", "id": "gsl_case_name"},
#                     "content": {"tag": "div", "id": "gs_opinion_wrapper"}
#                 }
#             },

#             DomainSource.CourtListener : {

#                 "url" : "https://www.courtlistener.com/",
#                 "method" : self.__scrape_webpage,
#                 "tags": {
#                     "title": {"tag": "h1", "class":""}, 
#                     "content": {"tag": "div", "class": "serif-text"}
#                 }
#             },

#             DomainSource.UsSupremeCourt : {

#                 "url" : "https://www.supremecourt.gov/",
#                 "method" : self.__extract_text_from_pdf,
#                 "tags": {}  # Not Needed, They are in PDF Format
#             },

#             DomainSource.HighCourtOfAustralia : {

#                 "url" : "https://www.hcourt.gov.au/",
#                 "method" : self.__extract_text_from_pdf,
#                 "tags": {}  # Not Needed, They are in PDF Format
#             }

#         }

   

#     def determine_domain_source(self, url):

#         for domain_source, source_info in self.url_mapper.items():

#             if url.startswith(source_info['url']):
#                 return domain_source
            
#         return None
    
#     def __get_soup(self, url, headers):
#         try:
#             page = requests.get(url, headers=headers)
#             page.raise_for_status()
#             return BeautifulSoup(page.text, 'lxml')
        
#         except requests.exceptions.HTTPError as e:
#             print("HTTP error occurred: ", e)
#             return None

#     def __save_content(self, title, content):

#         filename = f"{title}.txt"

#         filtered_filename = filename.replace(":", "").replace("/", "_").replace("\n"," ").replace("\r"," ").replace(" ", "_")

#         try:

#             with open(filtered_filename, "w", encoding='utf-8') as file:
#                 file.write(content)

#         except IOError as e:
#             print(f"An error occurred while saving the content: {e}")
            
#     def __extract_webpage_content(self, soup, tags):
        
#         title_tag = soup.find(tags['title']['tag'], class_= tags['title'].get('class'), id = tags['title'].get('id'))
#         content_tag = soup.find(tags['content']['tag'], class_ = tags['content'].get('class'), id = tags['content'].get('id'))

#         if title_tag and content_tag:
#             title = title_tag.text.strip()
#             content = content_tag.text.strip()
#             return title, content
#         else:
#             print("Could not find the title or content on the page.")
#             return None, None

#     def __scrape_webpage(self, url):

#         domain_source = self.determine_domain_source(url)

#         soup = self.__get_soup(url, headers=self.headers)

#         if soup:

#             tags = self.url_mapper[domain_source]["tags"]

#             title, content = self.__extract_webpage_content(soup, tags)

#             if title:
#                 print() 

#     def __extract_text_from_pdf(self, url):
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
            
#             doc = pymupdf.open(stream=response.content, filetype="pdf")
            
#             with open("output.txt", "wb") as out:  # use with-statement to handle file closing
#                 for page in doc:  # iterate the document pages
#                     text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
#                     out.write(text)  # write text of page
#                     out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
                    
#         except Exception as e:
#             print("Error: ", e)


#     def scrape(self, url):

#         domain_source = self.determine_domain_source(url)

#         if domain_source:
#             return self.url_mapper[domain_source]['method'](url)
#         else:
#             print("This website is not supported by the scraper.")


# if __name__=="__main__":
#     scrpay = Scraper()
#     #url = input()
#     scrpay.scrape(r"https://www.courtlistener.com/opinion/97635/graham-v-west-virginia/?q=graham&type=o&order_by=score%20desc&stat_Precedential=on")
    
###########HARVARD & COURT LISTENER ARE WORKING############

# import requests
# from bs4 import BeautifulSoup
# from enum import Enum
# import fitz  # PyMuPDF

# class DomainSource(Enum):
#     HarvardLawReview = 1
#     GoogleScholar = 2
#     LegiFrance = 3
#     CourtListener = 4
#     UsSupremeCourt = 5
#     HighCourtOfAustralia = 6

# class Scraper:
    
#     def __init__(self):
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
        
#         self.url_mapper = {
#             DomainSource.HarvardLawReview: {
#                 "url": "https://harvardlawreview.org/",
#                 "method": self._scrape_webpage,
#                 "tags": {
#                     "title": {"tag": "h1", "class": "single-article__title"},
#                     "content": {"tag": "div", "class": "entry-content"},
#                     "author_list": {"tag": "ul", "class": "single-article__authors-list"}
#                 }
#             },
#             DomainSource.GoogleScholar: {
#                 "url": "https://scholar.google.com/",
#                 "method": self._scrape_webpage,
#                 "tags": {
#                     "title": {"tag": "h3", "id": "gsl_case_name"},
#                     "content": {"tag": "div", "id": "gs_opinion_wrapper"}
#                 }
#             },
#             DomainSource.CourtListener: {
#                 "url": "https://www.courtlistener.com/",
#                 "method": self._scrape_webpage,
#                 "tags": {
#                     "title": {"tag": "h1", "class": ""},
#                     "author_header": {"tag": "span", "class": "meta-data-header", "string": "Author:"},
#                     "author_value": {"tag": "span", "class": "meta-data-value"},
#                     "content": {"tag": "div", "class": "serif-text"}
#                 }
#             },
#             DomainSource.UsSupremeCourt: {
#                 "url": "https://www.supremecourt.gov/",
#                 "method": self._extract_text_from_pdf,
#                 "tags": {}  # Not Needed, They are in PDF Format
#             },
#             DomainSource.HighCourtOfAustralia: {
#                 "url": "https://www.hcourt.gov.au/",
#                 "method": self._extract_text_from_pdf,
#                 "tags": {}  # Not Needed, They are in PDF Format
#             }
#         }

#     def determine_domain_source(self, url):
#         for domain_source, source_info in self.url_mapper.items():
#             if url.startswith(source_info['url']):
#                 return domain_source
#         return None
    
#     def _get_soup(self, url, headers):
#         try:
#             page = requests.get(url, headers=headers)
#             page.raise_for_status()
#             return BeautifulSoup(page.text, 'html.parser')
#         except requests.exceptions.HTTPError as e:
#             print("HTTP error occurred: ", e)
#             return None

#     def _extract_webpage_content(self, soup, tags):
#         title_tag = soup.find(tags['title']['tag'], class_=tags['title'].get('class'), id=tags['title'].get('id'))
#         content_tag = soup.find(tags['content']['tag'], class_=tags['content'].get('class'), id=tags['content'].get('id'))
        
#         if 'author_list' in tags:
#             authors = [a.text.strip() for a in soup.find(tags['author_list']['tag'], class_=tags['author_list'].get('class')).find_all('a')]
#             author = ', '.join(authors) if authors else 'No author found'
#         elif 'author_header' in tags and 'author_value' in tags:
#             author_header = soup.find(tags['author_header']['tag'], class_=tags['author_header'].get('class'), string=tags['author_header'].get('string'))
#             author = ''
#             if author_header:
#                 author_tag = author_header.find_next_sibling(tags['author_value']['tag'], class_=tags['author_value'].get('class'))
#                 author = author_tag.text.strip() if author_tag else 'No author found'
#         else:
#             author = 'No author found'
        
#         if title_tag and content_tag:
#             title = title_tag.text.strip()
#             return title, author
#         else:
#             print("Could not find the title, author, or content on the page.")
#             return None, None

#     def _scrape_webpage(self, url):
#         domain_source = self.determine_domain_source(url)
#         soup = self._get_soup(url, headers=self.headers)

#         if soup:
#             tags = self.url_mapper[domain_source]["tags"]

#             if domain_source == DomainSource.HarvardLawReview:
#                 # Extract title and authors based on HarvardLawReview specific tags
#                 title, author = self._extract_webpage_content(soup, tags)
#                 if title:
#                     print(f"Title: {title}")
#                     print(f"Author: {author}")
#                 else:
#                     print("Failed to extract metadata.")
#             elif domain_source == DomainSource.CourtListener:
#                 # Extract title and author based on CourtListener specific tags
#                 title_tag = soup.find('h1')
#                 author = self._extract_webpage_content(soup, tags)[1]  # Extract author specifically
#                 title = title_tag.text.strip() if title_tag else 'No title found'
#                 print(f"Title: {title}")
#                 print(f"Author: {author}")
#             else:
#                 # Extract title and author using generic logic for other domains
#                 title, author = self._extract_webpage_content(soup, tags)
#                 if title:
#                     print(f"Title: {title}")
#                     print(f"Author: {author}")
#                 else:
#                     print("Failed to extract metadata.")

#     def _extract_text_from_pdf(self, url):
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             doc = fitz.open(stream=response.content, filetype="pdf")
            
#             text_content = ""
#             for page in doc:
#                 text_content += page.get_text()
            
#             print(text_content)
#         except Exception as e:
#             print("Error: ", e)

#     def scrape(self, url):
#         domain_source = self.determine_domain_source(url)
#         if domain_source:
#             return self.url_mapper[domain_source]['method'](url)
#         else:
#             print("This website is not supported by the scraper.")

# if __name__ == "__main__":
#     scraper = Scraper()
#     scraper.scrape(r"https://harvardlawreview.org/blog/2023/09/reversing-remands-procedural-uncertainty-in-a-presidents-state-criminal-trials/")
#     scraper.scrape(r"https://www.courtlistener.com/opinion/96015/adams-v-new-york/?type=o&q=&type=o&order_by=score%20desc&stat_Precedential=on")
#     scraper.scrape(r"https://harvardlawreview.org/blog/2024/05/civil-suits-by-parents-against-family-policing-agencies/")
#     scraper.scrape(r"https://www.courtlistener.com/opinion/2196810/onti-inc-v-integra-bank/?type=o&q=%2Conty&type=o&order_by=score%20desc&stat_Precedential=on")

#######Attempting the GOOGLE SCHOLAR #########
import requests
from bs4 import BeautifulSoup
from enum import Enum
import fitz  # PyMuPDF

class DomainSource(Enum):
    HarvardLawReview = 1
    GoogleScholar = 2
    LegiFrance = 3
    CourtListener = 4
    UsSupremeCourt = 5
    HighCourtOfAustralia = 6

class Scraper:
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        self.url_mapper = {
            DomainSource.HarvardLawReview: {
                "url": "https://harvardlawreview.org/",
                "method": self._scrape_webpage,
                "tags": {
                    "title": {"tag": "h1", "class": "single-article__title"},
                    "content": {"tag": "div", "class": "entry-content"},
                    "author_list": {"tag": "ul", "class": "single-article__authors-list"}
                }
            },
            DomainSource.GoogleScholar: {
                "url": "https://scholar.google.com/",
                "method": self._scrape_webpage,
                "tags": {
                    "title": {"tag": "h3", "id": "gsl_case_name"},
                    "author": {"tag": "p", "text": "Supreme Court of United States."},
                    "content": {"tag": "div", "id": "gs_opinion_wrapper"}
                }
            },
            DomainSource.CourtListener: {
                "url": "https://www.courtlistener.com/",
                "method": self._scrape_webpage,
                "tags": {
                    "title": {"tag": "h1", "class": ""},
                    "author_header": {"tag": "span", "class": "meta-data-header", "string": "Author:"},
                    "author_value": {"tag": "span", "class": "meta-data-value"},
                    "content": {"tag": "div", "class": "serif-text"}
                }
            },
            DomainSource.UsSupremeCourt: {
                "url": "https://www.supremecourt.gov/",
                "method": self._extract_text_from_pdf,
                "tags": {}  # Not Needed, They are in PDF Format
            },
            DomainSource.HighCourtOfAustralia: {
                "url": "https://www.hcourt.gov.au/",
                "method": self._extract_text_from_pdf,
                "tags": {}  # Not Needed, They are in PDF Format
            }
        }

    def determine_domain_source(self, url):
        for domain_source, source_info in self.url_mapper.items():
            if url.startswith(source_info['url']):
                return domain_source
        return None
    
    def _get_soup(self, url, headers):
        try:
            page = requests.get(url, headers=headers)
            page.raise_for_status()
            return BeautifulSoup(page.text, 'html.parser')
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred: ", e)
            return None

    def _extract_webpage_content(self, soup, tags):
        title_tag = soup.find(tags['title']['tag'], class_=tags['title'].get('class'), id=tags['title'].get('id'))
        content_tag = soup.find(tags['content']['tag'], class_=tags['content'].get('class'), id=tags['content'].get('id'))
        
        if 'author_list' in tags:
            authors = [a.text.strip() for a in soup.find(tags['author_list']['tag'], class_=tags['author_list'].get('class')).find_all('a')]
            author = ', '.join(authors) if authors else 'No author found'
        elif 'author_header' in tags and 'author_value' in tags:
            author_header = soup.find(tags['author_header']['tag'], class_=tags['author_header'].get('class'), string=tags['author_header'].get('string'))
            author = ''
            if author_header:
                author_tag = author_header.find_next_sibling(tags['author_value']['tag'], class_=tags['author_value'].get('class'))
                author = author_tag.text.strip() if author_tag else 'No author found'
        elif 'author' in tags:
            author_tag = soup.find(tags['author']['tag'], string=tags['author'].get('text'))
            author = author_tag.text.strip() if author_tag else 'No author found'
        else:
            author = 'No author found'
        
        if title_tag and content_tag:
            title = title_tag.text.strip()
            return title, author
        else:
            print("Could not find the title, author, or content on the page.")
            return None, None

    def _scrape_webpage(self, url):
        domain_source = self.determine_domain_source(url)
        soup = self._get_soup(url, headers=self.headers)

        if soup:
            tags = self.url_mapper[domain_source]["tags"]

            if domain_source == DomainSource.HarvardLawReview:
                # Extract title and authors based on HarvardLawReview specific tags
                title, author = self._extract_webpage_content(soup, tags)
                if title:
                    print(f"Title: {title}")
                    print(f"Author: {author}")
                else:
                    print("Failed to extract metadata.")
            elif domain_source == DomainSource.CourtListener:
                # Extract title and author based on CourtListener specific tags
                title_tag = soup.find('h1')
                author = self._extract_webpage_content(soup, tags)[1]  # Extract author specifically
                title = title_tag.text.strip() if title_tag else 'No title found'
                print(f"Title: {title}")
                print(f"Author: {author}")
            elif domain_source == DomainSource.GoogleScholar:
                # Extract title and author based on GoogleScholar specific tags
                title, author = self._extract_webpage_content(soup, tags)
                print(f"Title: {title if title else 'No title found'}")
                print(f"Author: {author if author else 'No author found'}")
            else:
                # Extract title and author using generic logic for other domains
                title, author = self._extract_webpage_content(soup, tags)
                if title:
                    print(f"Title: {title}")
                    print(f"Author: {author}")
                else:
                    print("Failed to extract metadata.")

    def _extract_text_from_pdf(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            doc = fitz.open(stream=response.content, filetype="pdf")
            
            text_content = ""
            for page in doc:
                text_content += page.get_text()
            
            print(text_content)
        except Exception as e:
            print("Error: ", e)

    def scrape(self, url):
        domain_source = self.determine_domain_source(url)
        if domain_source:
            return self.url_mapper[domain_source]['method'](url)
        else:
            print("This website is not supported by the scraper.")

if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape(r"https://harvardlawreview.org/blog/2023/09/reversing-remands-procedural-uncertainty-in-a-presidents-state-criminal-trials/")
    scraper.scrape(r"https://www.courtlistener.com/opinion/97635/graham-v-west-virginia/?q=graham&type=o&order_by=score%20desc&stat_Precedential=on")
    scraper.scrape(r"https://scholar.google.com/scholar_case?case=913703117340005992&q=state&hl=en&as_sdt=2006")
