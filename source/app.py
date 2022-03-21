import logging
import sqlite3
import record
from gui import GUI
import stt
import random
logger = logging.getLogger(__name__)


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

    example_inputs = [
        "What time is it in London?",
        "What are the three laws of robotics?",
        "Does Santa Claus exist?",
        "How many calories are there in fudge?",
        "What is the distance between London and New York?",
        "Play loud noise",
        "Play door slam",
        "Play dog bark",
        "Play quiet music"
    ]

    sample_input = random.sample(example_inputs, len(example_inputs))[0].lower()
    print("sample input: " ,sample_input.lower())


    def process_speech():
        output = open("output.wav", "rb")
        results_from_stt = stt.speech_to_text(output)
        print("stt results: ", results_from_stt)
        return results_from_stt

    def play_audio():


    def app_state():
        if gui.gui_mode == "listening":
            gui.listening()
            record.record()
            gui.gui_mode = "answer"
            text_from_speech = process_speech()
            if text_from_speech.startswith("Play"):
                sound_request = text_from_speech[5:]
                # if sound_request == "music":



    # If no database available can insert data to play like this -
    # with open("sample.wav", "rb") as f:
    #    playQueue.put({"cmd": "load", "data": f.read()})

    gui.set_after(200, app_state)
    gui.run()
