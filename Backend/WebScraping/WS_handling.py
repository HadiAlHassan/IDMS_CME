from rest_framework.response import Response
from rest_framework.decorators import api_view
from WebScraping.ScrapingException import ScrapingException  # Ensure this import is correct

from Utils.decorators import timing_decorator
from WebScraping.Scraper import Scraper

@timing_decorator
@api_view(['POST'])
def scrape_website(request):
    url = request.data.get('url')
    if not url:
        return Response({'error': 'No URL provided'}, status=400)       
    try:
        scraper = Scraper()
        scraper.scrape(url)
        return Response({'message': 'Website scraped successfully'}, status=200)
    except ScrapingException as e:
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
