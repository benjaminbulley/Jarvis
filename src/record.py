import pyaudio
import wave
import logging
from time import sleep

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

logger = logging.getLogger(__name__)


def record(duration=5.0) -> bool:
    """ Uses Pyaudio to record an audio file in chucks
    :Param duration of the recording - 5 seconds
    """

    p = pyaudio.PyAudio()
    sleep(1.5)
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    logger.info("recording for %s seconds", duration)
    print("Recording audiofile")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    logger.info("done recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("../wav_files/output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return True

