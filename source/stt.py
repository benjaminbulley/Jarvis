import requests
import logging
from audio_player import player

logger = logging.getLogger(__name__)

subscription_key = '75f4ae5e6a6b46b7b5c69315f5c8dcbe'
region = 'uksouth'


def speech_to_text(sound_as_binary):
    """Sends the API request to convert speech to text.
    It expects sound as a wav file and returns the response object, which contains the text in:
    response["content"]["DisplayText"].
    See also response["content"]["RecognitionStatus"] for confirmation that it worked."""
    url = f'https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1'
    params = {"language": "en-GB"}
    headers = {
        "Content-Type": "audio/wav",
        "Accept": "application/json;text/xml",
        "Ocp-Apim-Subscription-Key": subscription_key,
        # 'Transfer-Encoding': 'chunked',
        # 'Connection': 'Keep-Alive',
        # 'Expect': '100-continue'
    }
    try:
        response = requests.post(url=url, params=params, data=sound_as_binary, headers=headers)
        print(response.json())
        return response.json().get("DisplayText")
    except requests.exceptions.ConnectionError:
        logging.error("Failed to establish a new connection")
        player.player_thread("cant_connect")


def process_speech():
    output = open("../wav_files/output.wav", "rb")
    results_from_stt = speech_to_text(output)
    print("stt results: ", results_from_stt)
    return results_from_stt
