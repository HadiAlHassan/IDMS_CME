import requests
from bs4 import BeautifulSoup
from enum import Enum
from pdf_utils import process_pdf

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

    def _clean_text(self, text):
        # Remove unnecessary newlines and extra spaces
        return ' '.join(text.split())

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
            title = self._clean_text(title_tag.text.strip())
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
                title = self._clean_text(title_tag.text.strip()) if title_tag else 'No title found'
                print(f"Title: {title}")
                print(f"Author: {author}") 
            elif domain_source == DomainSource.GoogleScholar:
                # Extract title and author based on GoogleScholar specific tags
                title, author = self._extract_webpage_content(soup, tags)
                print(f"Title: {title if title else 'No title found'}")
                print(f"Author: {author if author else 'No author found'}")
            elif domain_source in [DomainSource.UsSupremeCourt, DomainSource.HighCourtOfAustralia]:
                # Handle PDF URLs
                self._extract_text_from_pdf(url)
            else:
                # Extract title and author using generic logic for other domains
                title, author = self._extract_webpage_content(soup, tags)
                if title:
                    print(f"Title: {title} | Author: {author}")
                else:
                    print("Failed to extract metadata.")

    def _extract_text_from_pdf(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            with open("temp.pdf", "wb") as f:
                f.write(response.content)
            process_pdf("temp.pdf")
        else:
            print("Failed to download the PDF.")

    def scrape(self, url):
        domain_source = self.determine_domain_source(url)
        if domain_source is not None:
            self.url_mapper[domain_source]["method"](url)
        else:
            print("Could not determine the domain source.")

# Example usage
scraper = Scraper()
scraper.scrape(r"https://www.supremecourt.gov/orders/courtorders/070224zor_2co3.pdf")
scraper.scrape(r"https://harvardlawreview.org/blog/2023/09/reversing-remands-procedural-uncertainty-in-a-presidents-state-criminal-trials/")
scraper.scrape(r"https://www.courtlistener.com/opinion/97635/graham-v-west-virginia/?q=graham&type=o&order_by=score%20desc&stat_Precedential=on")
scraper.scrape(r"https://scholar.google.com/scholar_case?case=913703117340005992&q=state&hl=en&as_sdt=2006")
