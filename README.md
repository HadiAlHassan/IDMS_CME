# Scraper.py Documentation

Scraper.py represents the API for webscraping approved websites for content and storing them in a TXT file.

The process of scraping is done with one of Three ways here:
1. Using BeautifulSoup4 and requests, where we request the web pafe and extract the contents
2. Using selenium to automate the process of copying the data.
3. Extracting Text from a PDF.
------------------------------------------------------------------------------------------------------------------------------
## Prerequisutes to Use the Scraper.py File.

pip install the requirements.TXT file (Mainly selenium Beautifulsoup4 requests lxml and pymupdf)

For selenium you must install the suitable chrome driver (more details here https://pypi.org/project/selenium/)
------------------------------------------------------------------------------------------------------------------------------
## Approved websites so far and their respective method to scrape (denoted by the number above):
1.HarvardLawReview (1)
2.GoogleScholar (1)
3.LegiFrance (2)
4.CourtListener (1) 
5.UsSupremeCourt (3)
6.HighCourtOfAustralia (3) 




------------------------------------------------------------------------------------------------------------------------------

## Breakdown of the Classes and Methods
Scraper.py Contains two classes:
**Source** and **Scraper**

### Source Class

Used to seamlessly classify domains and automatically select which function to scrape from, depending on the domain.

### Scraper Class

the **__init__** method contains 3 elements:
1. _Source_ which uses the source class mentioned above
2. _Headers_ The headers we use when requesting webpages using the requests library. (An HTTP Get request contains a header about the browser)
3. _URL_Mapper_ As the name suggests, used to map a url to its respective domain function.

### Scraping Mechanism
Web pages are structured with HTML, web scrapers take the text from between the HTML text, and extract them (i.e, "Scrape them")

In this file we scrape as follows,
**1. With Beautifulsoup and Requests:** 

1.1 Webpage is requested via the requests library
1.2 Scraper is readied with BeautifulSoup by creating a **BeautifulSoup** object
1.3 Specified sections of the website are extracted
1.4 A .TXT file is created, and the contents are copied into it

**2. With Selenium** 

2.1 Initializing a Driver
2.2 Retrieiving a Webpage with _Driver.get()_ method
2.3 extracting the content into the TXT file

------------------------------------------------------------------------------------------------------------------------------
## Breakdown of methods:
### Small Methods:
- `setup_driver`: sets up the selenium driver
-  `determine_Source`: Used to determine the source of the URL to decide which function to use to scrape
-  `get_soup`: Retreives the webpage and returns the contents of the extracted HTML page.
-  `save_content`: Saves the content into a TXT file
-  `extract_content_Byclass` and `extract_content_Byid`: does the actual extraction part of the webscraping feature.

### Domain Specific Scraping methods:
**BeautifulSoup and Requests**
Most of the functions perform the same inner methods, but differ by the HTML Tags that we are selecting.
They follow the same algorithm:
```
soup = self.get_soup(url, headers=self.headers)

        if soup:
            tags = self.Url_Mapper[Source.CourtListener]["tags"]
            title, content = self.extract_content_Byclass(soup, tags)
            if title and content:
                self.save_content(title, content)
```


