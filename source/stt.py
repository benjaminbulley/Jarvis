import requests
import base64
import json
import time
import logging

# subscriptionKey = "8025156711b145b69576a9a63c80f198"
subscriptionKey = "00487878-43e4-4427-a4d7-8cf15f33a069"
region = "uksouth"

# a common wave header, with zero audio length
# since stream data doesn't contain header, but the API requires header to fetch format information, so you need post this header as first chunk for each query
WaveHeader16K16BitMono = bytes(
    [82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18, 0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0, 125,
     0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0])


# a generator which reads audio data chunk by chunk
# the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
def get_chunk(path, chunk_size=1024):
    yield WaveHeader16K16BitMono
    while True:
        time.sleep(chunk_size / 32000)  # to simulate human speaking rate
        chunk = path.read(chunk_size)
        if not chunk:
            global upload_finish_time
            upload_finish_time = time.time()
            break
        yield chunk


# build pronunciation assessment parameters
referenceText = "Good morning."
pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\"}" % referenceText
pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

# build request
url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-us" % region
headers = {'Accept': 'application/json;text/xml',
           'Connection': 'Keep-Alive',
           'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
           'Ocp-Apim-Subscription-Key': subscriptionKey,
           'Pronunciation-Assessment': pronAssessmentParams,
           'Transfer-Encoding': 'chunked',
           'Expect': '100-continue'}


# send request with chunked data
def stt(path):
    response = requests.post(url=url, data=get_chunk(path), headers=headers)
    get_response_time = time.time()
    path.close()

    result_json = json.loads(response.text)
    print(json.dumps(result_json, indent=4))

    latency = get_response_time - upload_finish_time
    print("Latency = %sms" % int(latency * 1000))

stt(path)
