from googletrans import Translator


def getTranslatedText(message):
    translator = Translator()
    text = translator.translate(message).text
    return text
