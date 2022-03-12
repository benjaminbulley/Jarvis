import requests
import logging
from source.player import Player

logging.basicConfig(level=logging.DEBUG)

say = "Hi, I'm your assistant! How can I help?"

p = Player()


def tts(text):
    key = "00487878-43e4-4427-a4d7-8cf15f33a069"
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

    # with open("../wav_files/hello.wav", "wb") as out:
    #     out.write(response.content)

    p.play(response.content)


tts(say)
