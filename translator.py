
#  $ pip install -U textblob

from textblob import TextBlob
from googletrans import Translator


def translate(string):
    return translateByGoogleTranslate(string)
    # return translateByBlob(string)

def translateByBlob(string):
    try:
        blob = TextBlob(string)
        responce = str(blob.translate(from_lang='en', to='ru'))
    except Exception as err:
        Error = f'translate({string})\nError:' + str(err)
        print(Error)
        return Error
    return responce

def translateByGoogleTranslate(string):
    try:
        translator = Translator()
        responce = translator.translate(string, dest='ru')
    except Exception as err:
        Error = f'translate({string})\nError:' + str(err)
        print(Error)
        return Error
    return responce.text


if __name__ == '__main__':
    print(translate("Good morning!!!"))
    print(translate("Buongiorno!"))