import logging
import sqlite3
import threading
import record
from sounds_db import SoundDB
from gui import GUI
from player import Player
from query_wolframalpha import query
from stt import process_speech
from tts import text_speech, didnt_understand

logger = logging.getLogger(__name__)


def play_audio(play_request):
    if play_request == "music":
        music = SoundDB.get_music(cur)
        Player.play(music)
    elif play_request.startswith == "loud":
        loud_sound = SoundDB.get_loud_sound()


play_thread = threading.Thread(target=play_audio, args=(1,), daemon=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Starting")
    # Create the GUI, but don't run mainloop() yet
    gui = GUI("app")
    db_con = sqlite3.connect("sounds.db")
    cur = db_con.cursor()

    # Note that we can access methods and properties of the gui
    # because this main thread is the gui thread.  We should not
    # directly access objects in other threads.

    print("gui mode", gui.gui_mode)


    def app_state():
        if gui.gui_mode == "listening":
            gui.listening()
            record.record()
            text_from_speech = process_speech()
            if text_from_speech is None:
                didnt_understand()
            elif text_from_speech.startswith("Play"):
                sound_request = text_from_speech[5:]
                play_audio(sound_request)
            else:
                wolframalpha_response = query(text_from_speech)
                text_speech(wolframalpha_response)
                gui.gui_mode = "answer"
        else:
            gui.gui_mode = "listening"


    gui.set_after(200, app_state)
    gui.run()
