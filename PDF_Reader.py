import pymupdf
import requests

def Extract_Text_PDF(link):
    doc = pymupdf.open(link) # open a document    
    out = open("output.txt", "wb") # create a text output

    for page in doc: # iterate the document pages
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
        out.write(text) # write text of page
        out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
    
    out.close() # close the output file
    return

def Extract_Text_PDF_URL(url):
    try:
        response = requests.get(url)
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
        return



if __name__ == "__main__":
    #link = "commonwealthvgraham.pdf"
    #Extract_Text_PDF(link)
    #url = "https://www.supremecourt.gov/pdfs/transcripts/1984/84-849_04-16-1985.pdf"
    #url = "https://eresources.hcourt.gov.au/downloadPdf/2024/HCA/23"
    #Extract_Text_PDF_URL(url)

