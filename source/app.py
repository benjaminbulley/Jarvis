import logging

import record
from source.gui import GUI
from time import sleep
import stt
import random
import query_wolframalpha
from threading import Thread
from sounds_db import SoundDB

from source.player import Player

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


class DBTread(Thread):
    """
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=True):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.args = args
        self.kwargs = kwargs
        # Open DB in read-only mode
        self.db = SoundDB("file:music.db?mode=ro")

    def run(self):
        """
        """
        queue_in: Queue = self.args[0]
        queue_out: Queue = self.args[1]
        while True:
            msg = queue_in.get()
            queue_in.task_done()
            if msg["cmd"] == "albums":
                albums = self.db.get_album_names()
                queue_out.put({"from": "db", "cmd": "albums", "data": albums})
            elif msg["cmd"] == "tracks":
                tracks = self.db.get_track_names(msg["data"])
                queue_out.put({"from": "db", "cmd": "tracks", "data": tracks})
            elif msg["cmd"] == "content":
                content = self.db.get_content(msg["data"])
                queue_out.put({"from": "db", "cmd": "content", "data": content})

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.debug("Starting")
    # Create the GUI, but don't run mainloop() yet
    gui = GUI("app")

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
    print(sample_input.lower())


    def process_speech():
        output = open("path_of_file.wav", "rb")
        results_from_stt = stt.stt(output).lower()
        print(results_from_stt)


    def process_input(some_input):
        if some_input.startswith("play"):
            print("tbd")
        else:
            wolframalpha_response = query_wolframalpha.query(some_input)


    def gui_state():
        if gui.gui_mode == "listening":
            gui.listening()
            record.record()
            gui.gui_mode = "answer"
            if gui.gui_mode == "answer":
                process_speech()


    # If no database available can insert data to play like this -
    # with open("sample.wav", "rb") as f:
    #    playQueue.put({"cmd": "load", "data": f.read()})

    gui.set_after(200, gui_state)
    gui.run()
