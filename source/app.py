"""
Welcome to Jarvis, your personal assistant
==========================================
The application entry point.
Run this module to use the user interface to interact with Jarvis
"""
import logging
import sqlite3
import record
from player_logic import play_audio
from gui import GUI
from query_wolframalpha import wolfram_query
from stt import process_speech
from tts import text_speech
from audio_player import player


logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Starting")
    # Create the GUI, but don't run mainloop() yet
    gui = GUI("Jarvis")
    db_con = sqlite3.connect("sounds.db")
    cur = db_con.cursor()

    # player_thread.start()

    print("gui mode", gui.gui_mode)


    def app_state():
        """
        State change in our application occurs here.
        """
        if gui.gui_mode == "listening":
            gui.listening()
            record.record()
            text_from_speech = process_speech()
            if text_from_speech is None:
                pass
            # play_audio("didnt_understand")
            elif text_from_speech.startswith("Play"):
                gui.gui_mode = "play"
                play_audio(text_from_speech)
                gui.gui_mode = "listening"
            else:
                gui.gui_mode = "answer"
                wolframalpha_response = wolfram_query(text_from_speech)
                text_speech(wolframalpha_response)
                gui.gui_mode = "listening"

    """
    Connect this module to the fornt end.
    """
    gui.set_after(200, app_state)  # run after stated milliseconds
    gui.run()
