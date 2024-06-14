import requests
from bs4 import BeautifulSoup


def get_doc_scholar(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    soup.find_all('div',"gs_opinion_wrapper")

    with open("output.txt", "w") as f:
        f.write(str(soup.text))

    return


if __name__ == "__main__":
    url = "https://scholar.google.com/scholar_case?case=913703117340005992&q=state&hl=en&as_sdt=2006"
    print(get_doc_scholar(url))