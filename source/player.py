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
#     def play(self, audio_in: any):
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
On dealine day I'm having to switch out pyaudio with pydub which seems to work only with local files.
Im getting an error with pyaudio as :  UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 4942:
 character maps to <undefined>
"""
import threading
from pydub import AudioSegment
from pydub.playback import play
import logging
import simpleaudio as sa

logger = logging.getLogger(__name__)


def play(audio_data):
    sa.play_buffer(audio_data, 2, 2, 44100)


def player_local(path: str):
    """
    this function plays local files with the help pf pydub
    """
    f = AudioSegment.from_wav(path)
    play(f)


def player_thread_local(audio_in):
    thread = threading.Thread(target=lambda y=audio_in: player_local(y), daemon=True)
    thread.start()


def player_thread(blob):
    thread = threading.Thread(target=lambda y=blob: play(y), daemon=True)
    thread.start()

