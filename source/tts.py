import requests
import logging
from source.play import play

logging.basicConfig(level=logging.DEBUG)

say = "How was your day??"


def tts(text):
    key = "aec62efd1ccd427f886ca2ca1a1a47a6"
    region = "uksouth"

    url = f'https://{region}.tts.speech.microsoft.com/cognitiveservices/v1'

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-16khz-16bit-mono-pcm'
        # RIFF is also known as WAV.
        # Other formats are supported by the Azure API but will require decoding
        # before playing. e.g. 'audio-16khz-128kbitrate-mono-mp3'
    }
    # voice = "en-US-GuyRUS"
    # voice = "ms-MY-YasminNeural"
    voice = "en-US-EricNeural"

    data = f"""
    <speak version='1.0' xml:lang='en-US'>
     <voice xml:lang='en-US' xml:gender='Male' name='{voice}'>{text}</voice>
    </speak>"""

    response = requests.post(url, data=data, headers=headers)

    logging.info(str(response))

    # Requests return binary content in response.content
    # If the data was zipped by the server, requests will unzip it by default.
    # https://docs.python-requests.org/en/master/user/quickstart/#binary-response-content

    # with open("hello.wav", "wb") as out:
    #    out.write(response.content)

    play(response.content)


tts(say)
