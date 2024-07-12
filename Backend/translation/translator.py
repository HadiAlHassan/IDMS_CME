from deep_translator import GoogleTranslator
from lang_detector import LanguageDetector
from translation_exception import TranslationException

class Translator:

    def __init__(self):
        pass

    def translate(self, text: str, target_lang: str) -> str:

        source_language = LanguageDetector().detect_language(text = text)

        if source_language == target_lang:
            return text
        try:
            return GoogleTranslator(source= source_language, target = target_lang).translate(text)
        
        except Exception as e:
            raise TranslationException(str(e))
        
    def get_supported_languages(self):
        langs_list = GoogleTranslator().get_supported_languages()
        return langs_list

    def get_supported_languages_as_dict(self):
        langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        return langs_dict

if __name__ == '__main__':
    translator = Translator()
    print(translator.translate('Hello', 'es'))


