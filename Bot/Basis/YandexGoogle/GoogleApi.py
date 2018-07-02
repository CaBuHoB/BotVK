from googletrans import Translator


def getTranslatedText(message):
    translator = Translator()
    return translator.translate(message).text
