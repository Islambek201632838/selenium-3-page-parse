from googletrans import Translator

class TextTranslator:
    def __init__(self, src='en', dest='ru'):
        self.translator = Translator()
        self.src = src
        self.dest = dest

    def translate_text(self, text):
        try:
            return self.translator.translate(text, src=self.src, dest=self.dest).text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
