import threading
import pyaudio
import wave
import io
import logging

logger = logging.getLogger(__name__)


class Player:
    CHUNK = 1024

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self._wf = None
        self.paused = False

    def close(self):
        """ Accepts audio in as blob and streams it through the speakers
        """
        # close PyAudio
        logger.warning("close")
        self.p.terminate()

    def play(self, audio_in: any):
        """ Accepts audio in as blob and streams it through the speakers
        :param audio_in (any) is either a path to a WAV file or bytes containing WAV audio.
        """
        try:
            if type(audio_in) == type(b''):
                wf = wave.open(io.BytesIO(audio_in), 'rb')
            else:
                wf = wave.open(audio_in, 'rb')

            stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                                 channels=wf.getnchannels(),
                                 rate=wf.getframerate(),
                                 output=True)
            data = wf.readframes(Player.CHUNK)
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(Player.CHUNK)
            stream.stop_stream()
            stream.close()
        except FileNotFoundError:
            logger.error("File not found")

    # @staticmethod
    # def player():
    #     player.play(audio_in)

    def player_thread(self, audio_in):
        thread = threading.Thread(target=lambda y=audio_in: self.play(y), daemon=True)
        thread.start()

player = Player()  # instantiating singleton


