from WebScraping.Scraper import Scraper
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Utils.decorators import timing_decorator

@timing_decorator
@api_view(['POST'])
def scrape_website(request):
    url = request.data.get('url')
    if not url:
        return Response({'error': 'No URL provided'}, status=400)   
    try:
        scraper = Scraper()
        scraper.Scrape(url)
        return Response({'message': 'Website scraped successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
