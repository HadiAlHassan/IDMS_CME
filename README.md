# Scraper.py Documentation

## Prerequisites to Use Scraper.py

The required packages include:

- selenium
- BeautifulSoup4
- requests
- lxml
- pymupdf
- pyperclip  

For Selenium, you must install the suitable Chrome driver. More details can be found [here](https://pypi.org/project/selenium/).

## Approved Websites and Their Respective Scraping Methods

1. **HarvardLawReview** (Method 1: BeautifulSoup and requests)
2. **GoogleScholar** (Method 1: BeautifulSoup and requests)
3. **LegiFrance** (Method 2: Selenium)
4. **CourtListener** (Method 1: BeautifulSoup and requests)
5. **UsSupremeCourt** (Method 3: Extracting text from PDF)
6. **HighCourtOfAustralia** (Method 3: Extracting text from PDF)

## Breakdown of Classes and Methods

### Domain_Source Enum

The `Domain_Source` enum classifies domains and helps in automatically selecting which function to use for scraping based on the domain.

### Scraper Class

#### `__init__` Method

Contains three elements:

- **Source**: Uses the `Domain_Source` class for domain classification.
- **Headers**: The headers used when requesting webpages via the requests library. These headers mimic an HTTP GET request from a browser.
- **URL Mapper**: Maps a URL to its respective domain function.

### Scraping Mechanism

Web pages are structured with HTML. Web scrapers extract the text between HTML tags. The scraper in this file performs scraping using the following methods:

#### 1. With BeautifulSoup and Requests

1. Requests the webpage via the requests library.
2. Prepares the scraper using BeautifulSoup by creating a `BeautifulSoup` object.
3. Extracts specified sections of the website.
4. Creates a .TXT file and copies the contents into it.

#### 2. With Selenium

1. Initializes a Selenium driver.
2. Retrieves a webpage with the `driver.get()` method.
3. Extracts the content into a TXT file.

### Breakdown of Methods

#### Small Methods

- `__setup_driver`: Sets up the Selenium driver.
- `determine_domain_source`: Determines the source of the URL to decide which function to use for scraping.
- `get_soup`: Retrieves the webpage and returns the contents of the extracted HTML page.
- `save_content`: Saves the content into a TXT file.
- `extract_webpage_content`: Extracts content by HTML class or ID tags.

#### Domain-Specific Scraping Methods

**BeautifulSoup and Requests**

Most functions perform the same internal methods but differ by the HTML tags they select. The general algorithm is:

```python
soup = self.get_soup(url, headers=self.headers)
if soup:
    tags = self.url_mapper[domain_source]["tags"]
    title, content = self.extract_webpage_content(soup, tags)
    if title and content:
        self.save_content(title, content)
