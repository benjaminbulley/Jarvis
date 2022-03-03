import os
import requests

key = "8025156711b145b69576a9a63c80f198"
region = os.getenv("AZURE_REGION", "uksouth")

headers = {
    'Ocp-Apim-Subscription-Key': key
}

url = f'https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list'


def get_voices():
    r = requests.get(url, headers=headers)
    voice_list = []

    for voice in r.json():
        voice_list.append(voice['ShortName'])
    return voice_list


if __name__ == "__main__":
    voice_list = get_voices()
    print(voice_list)
