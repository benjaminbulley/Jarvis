import logging
import sqlite3
import time

import record
from source.gui import GUI
from time import sleep
import stt
import random
import query_wolframalpha
from threading import Thread
from sounds_db import SoundDB as db
from source.player import Player
from play_random import random_clip

logger = logging.getLogger(__name__)


class PlayerThread(Thread):
    """
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=True):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.args = args
        self.kwargs = kwargs
        self.player = Player()
        self.player.paused = True

    def run(self):
        """
        """
        while True:






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
        output = open("path_of_file.wav", "rb")
        results_from_stt = stt.stt(output)
        print("stt results: ", results_from_stt)
        return results_from_stt


    def app_state():
        if gui.gui_mode == "listening":
            gui.listening()
            record.record()
            gui.gui_mode = "answer"
            # text_from_speech = process_speech()
            text_from_speech = sample_input
            if text_from_speech.startswith("Play"):
                sound_request = text_from_speech[:5]
                if sound_request == "music":







    # If no database available can insert data to play like this -
    # with open("sample.wav", "rb") as f:
    #    playQueue.put({"cmd": "load", "data": f.read()})

    gui.set_after(200, app_state)
    gui.run()
