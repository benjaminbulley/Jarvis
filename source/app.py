import logging

import record
from source.gui import GUI
from time import sleep
import stt
import random
import query_wolframalpha

logger = logging.getLogger(__name__)

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

    def process_input(sample_input):
        if "play" in sample_input:
            None # TBC



    def body():
        if gui.gui_mode == "listening":
            gui.listening()
            record.record()
            gui.gui_mode = "answer"
            if gui.gui_mode == "answer":
                process_speech()


    # If no database available can insert data to play like this -
    # with open("sample.wav", "rb") as f:
    #    playQueue.put({"cmd": "load", "data": f.read()})

    gui.set_after(200, body)
    gui.run()
