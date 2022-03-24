import logging
import sqlite3
import threading
import record
from player_logic import player_thread
from gui import GUI
from query_wolframalpha import wolfram_query
from stt import process_speech
from tts import text_speech

logger = logging.getLogger(__name__)

#
# def player_thread(text_from_speech):
#     thread = threading.Thread(target=lambda x=text_from_speech: play_audio(x), daemon=True)
#     return thread


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Starting")
    # Create the GUI, but don't run mainloop() yet
    gui = GUI("app")
    db_con = sqlite3.connect("sounds.db")
    cur = db_con.cursor()

    # player_thread.start()

    print("gui mode", gui.gui_mode)


    def app_state():
        if gui.gui_mode == "listening":
            gui.listening()
            record.record()
            text_from_speech = process_speech()
            if text_from_speech is None:
                player_thread("didnt_understand")
            elif text_from_speech.startswith("Play"):
                gui.gui_mode = "play"
                player_thread(text_from_speech)
            else:
                gui.gui_mode = "answer"
                wolframalpha_response = wolfram_query(text_from_speech)
                text_speech(wolframalpha_response)


    gui.set_after(200, app_state)
    gui.run()
