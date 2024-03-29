import requests #http 요청 처리를 하게 해주는 모듈

def ocr_space_url(url, overlay=False, api_key='helloworld', language='kor'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


test_url = ocr_space_url(
    url='https://pbs.twimg.com/media/D40ltyCX4AE3Ffx?format=jpg&name=medium')
print(test_url)


