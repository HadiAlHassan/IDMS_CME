import os
from dotenv import load_dotenv
import detectlanguage
from detection_exception import DetectionException

load_dotenv()

class LanguageDetector:
    def __init__(self):

        api_key = os.getenv("DETECT_LANGUAGE_API_KEY")
        if not api_key:
            raise DetectionException("API key not found\nPlease configure your .env file")
            
        detectlanguage.configuration.api_key = api_key
        
        #Secure mode (SSL) for passing sensitive data
        detectlanguage.configuration.secure = True

    def detect_language(self, text):
        try:
            return detectlanguage.detect(text)[0].get('language')
            
        except Exception as e:
            raise DetectionException(str(e))



if __name__ == "__main__":
    detector = LanguageDetector()
    text = "Hello, how are you?"
    result = detector.detect_language(text)
    print(result)