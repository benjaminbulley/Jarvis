import logging
import record
from source.gui import GUI
from time import sleep
import stt

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


    def process_speech():
        output = open("path_of_file.wav", "rb")
        results_from_stt = stt.stt(output)
        print(results_from_stt)


    def body():
        if gui.gui_mode == "listening":
            record.record()
            gui.gui_mode = "answer"
            if gui.gui_mode == "answer":
                process_speech()


    # If no database available can insert data to play like this -
    # with open("sample.wav", "rb") as f:
    #    playQueue.put({"cmd": "load", "data": f.read()})

    gui.set_after(200, body)
    gui.run()
