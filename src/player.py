# import threading
# import pyaudio
# import wave
# import io
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# class Player:
#     CHUNK = 1024
#
#     def __init__(self):
#         self.p = pyaudio.PyAudio()
#         self._wf = None
#         self.paused = False
#
#     def close(self):
#         """ Accepts audio in as blob and streams it through the speakers
#         """
#         # close PyAudio
#         logger.warning("close")
#         self.p.terminate()
#
#     def play1(self, audio_in: any):
#         """ Accepts audio in as blob and streams it through the speakers
#         :param audio_in (any) is either a path to a WAV file or bytes containing WAV audio.
#         """
#         try:
#             if type(audio_in) == type(b''):
#                 wf = wave.open(io.BytesIO(audio_in), 'rb')
#             else:
#                 wf = wave.open(audio_in, 'rb')
#
#             stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
#                                  channels=wf.getnchannels(),
#                                  rate=wf.getframerate(),
#                                  output=True)
#             data = wf.readframes(Player.CHUNK)
#             while len(data) > 0:
#                 stream.write(data)
#                 data = wf.readframes(Player.CHUNK)
#             stream.stop_stream()
#             stream.close()
#         except FileNotFoundError:
#             logger.error("File not found")
# -
#     # @staticmethod
#     # def player():
#     #     player.play(audio_in)
#
#     def player_thread(self, audio_in):
#         thread = threading.Thread(target=lambda y=audio_in: self.play(y), daemon=True)
#         thread.start()
#
# player = Player()  # instantiating singleton
#
#
####################################################################################
"""
Switching out pyaudio last minute with pydub to play local files and simple audio to play bytes.
I'm getting an error with pyaudio as :  UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 4942:
 character maps to <undefined>

"""
import threading
from pydub import AudioSegment
from pydub.playback import play
import logging
import simpleaudio as sa

logger = logging.getLogger(__name__)


def play_blob(audio_data: any):
    """
    Uses pydub to play audio, specifying sample rate
    :params
    """
    sa.play_buffer(audio_data, 2, 2, 44100)


def play_wav(path: str):
    """
    this function plays local files with the help of pydub
    :params path (str)- path to wav file
    """
    f = AudioSegment.from_wav(path) # use AudioSegment to unpack the file from the path
    play(f)


def player_thread_local(path: str):
    """
    threads the local file play_wav function, this is what prevents the ui from blocking when something is playing
    :params path  (str)- path to wav file
    """
    thread = threading.Thread(target=lambda y=path: play_wav(y), daemon=True)
    thread.start()


def player_thread(blob: any):
    """
    threads the local file
    :params path  (blob)- bytes file from database
    """
    thread = threading.Thread(target=lambda y=blob: play_blob(y), daemon=True)
    thread.start()

