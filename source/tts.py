import requests
import logging

from player_logic import player_thread

logging.basicConfig(level=logging.DEBUG)


def text_speech(text):
    key = "75f4ae5e6a6b46b7b5c69315f5c8dcbe"
    region = "uksouth"
    url = f'https://{region}.tts.speech.microsoft.com/cognitiveservices/v1'

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-16khz-16bit-mono-pcm',

        # RIFF is also known as WAV.
        # Other formats are supported by the Azure API but will require decoding
        # before playing. e.g. 'audio-16khz-128kbitrate-mono-mp3'
    }

    voice = "en-US-EricNeural"

    data = f"""
    <speak version='1.0' xml:lang='en-US'>
    <voice xml:lang='en-US' xml:gender='Male' name='{voice}'>{text}</voice>
    </speak>"""

    response = requests.post(url, data=data, headers=headers)
    print('response', response)

    logging.info(str(response))

    # Requests returns binary content in response.content
    # If the data was zipped by the server, requests will unzip it by default.
    # https://docs.python-requests.org/en/master/user/quickstart/#binary-response-content

    with open("../wav_files/output.wav", "wb") as out:
        out.write(response.content)

    player_thread("output")


if __name__ == "__main__":
    text = "Check your Internet Connection"
    text_speech(text)

