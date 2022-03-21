import pyaudio
import wave
import io
import sqlite3
import logging

logger = logging.getLogger(__name__)


class Player:
    CHUNK = 1024

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self._wf = None
        self.paused = False

    def close(self):
        # close PyAudio
        logger.warning("close")
        self.p.terminate()

    def play(self, audio_in: any):
        """
        audio_in is either a path to a WAV file or bytes containing WAV audio.
        """
        if type(audio_in) == type(b''):
            wf = wave.open(io.BytesIO(audio_in), 'rb')
        else:
            wf = wave.open(audio_in, 'rb')

        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)

        # read data
        data = wf.readframes(Player.CHUNK)

        # play stream
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(Player.CHUNK)

        # stop stream
        stream.stop_stream()
        stream.close()


if __name__ == "__main__":
    p = Player()
    with open("../wav_files/Left_hand_free.wav", "rb") as f:
        p.play(f)
