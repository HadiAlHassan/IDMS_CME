import requests
from bs4 import BeautifulSoup
from enum import Enum
from transformers import BartForConditionalGeneration, BartTokenizer
import time
from concurrent.futures import ThreadPoolExecutor
import torch
import re
 
class DomainSource(Enum):
    HarvardLawReview = 1
    GoogleScholar = 2
    CourtListener = 3
 
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
                    "author_list": {"tag": "ul", "class": "single-article__authors-list"},
                    "content": {"tag": "div", "class": "entry-content"}
                }
            },
            DomainSource.GoogleScholar: {
                "url": "https://scholar.google.com/",
                "method": self._scrape_webpage,
                "tags": {
                    "title": {"tag": "h3", "id": "gsl_case_name"},
                    "author": {"tag": "p", "text": "Supreme Court of United States."},
                    "content": {"tag": "div", "id": "gs_opinion"}
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
            }
        }
       
        # Initialize BART model and tokenizer
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
 
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
            print(f"HTTP error occurred: {e}")
            return None
 
    def _clean_text(self, text):
        text = re.sub(r'(\w+)\s*v\.\s*(\w+)', r'\1 v. \2', ' '.join(text.split()))
        return text.title()  # Capitalize the first letter of each word in the title
 
    def _extract_webpage_content(self, soup, tags):
        # Extract title
        title_tag = soup.find(tags['title']['tag'], class_=tags['title'].get('class'), id=tags['title'].get('id'))
        title = self._clean_text(title_tag.get_text(strip=True)) if title_tag else 'No title found'
 
        # Extract author
        if 'author_list' in tags:
            author_list = soup.find(tags['author_list']['tag'], class_=tags['author_list'].get('class'))
            if author_list:
                authors = [a.get_text(strip=True) for a in author_list.find_all('a')]
                author = ', '.join(authors) if authors else 'No author found'
            else:
                author = 'No author found'
        elif 'author_header' in tags and 'author_value' in tags:
            author_header = soup.find(tags['author_header']['tag'], class_=tags['author_header'].get('class'), string=tags['author_header'].get('string'))
            author = ''
            if author_header:
                author_tag = author_header.find_next_sibling(tags['author_value']['tag'], class_=tags['author_value'].get('class'))
                author = self._clean_text(author_tag.get_text(strip=True)) if author_tag else 'No author found'
        elif 'author' in tags:
            author_tag = soup.find(tags['author']['tag'], string=tags['author'].get('text'))
            author = self._clean_text(author_tag.get_text(strip=True)) if author_tag else 'No author found'
        else:
            author = 'No author found'
       
        # Extract content
        content_tag = soup.find(tags['content']['tag'], class_=tags['content'].get('class'), id=tags['content'].get('id'))
        content = self._clean_text(content_tag.get_text(separator=' ', strip=True)) if content_tag else 'No content found'
       
        # Summarize the content
        summary = self.summarize_content(content)
       
        return {
            "title": title,
            "author": author,
            "summary": summary
        }
 
    def _scrape_webpage(self, url):
        domain_source = self.determine_domain_source(url)
        soup = self._get_soup(url, headers=self.headers)
 
        if soup:
            tags = self.url_mapper[domain_source]["tags"]
            return self._extract_webpage_content(soup, tags)
        else:
            return None
 
    def summarize_content(self, content):
        tokens = self.tokenizer(content, max_length=1024, return_tensors='pt', truncation=True)
        input_ids = tokens['input_ids'][0]
        attention_mask = tokens['attention_mask'][0]
 
        max_chunk_size = 1024
        chunk_size = max_chunk_size - 100
        overlap = 50
        chunks = []
        for i in range(0, len(input_ids), chunk_size - overlap):
            chunks.append((input_ids[i:i + chunk_size], attention_mask[i:i + chunk_size]))
 
        def summarize_chunk(chunk):
            input_ids_chunk, attention_mask_chunk = chunk
            inputs = {'input_ids': input_ids_chunk.unsqueeze(0), 'attention_mask': attention_mask_chunk.unsqueeze(0)}
            with torch.no_grad():
                summary_ids = self.model.generate(
                    inputs['input_ids'],
                    max_length=150,
                    min_length=30,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True
                )
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
 
        num_threads = 2  
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            summaries = list(executor.map(summarize_chunk, chunks))
 
        combined_summary = ' '.join(summaries)
        if not combined_summary.endswith('.'):
            combined_summary += '.'
       
        return combined_summary
 
    def scrape(self, url):
        start_time = time.time()
        domain_source = self.determine_domain_source(url)
        if domain_source is not None:
            result = self.url_mapper[domain_source]["method"](url)
        else:
            result = None
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total scraping time: {total_time:.2f} seconds.")
        return result