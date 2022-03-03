import logging
from threading import Thread
class Player(Thread):
    """
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, daemon=True):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.args = args
        self.kwargs = kwargs
        self.player = WavPlay()
        self.player.paused = True

    def run(self):
        """
        """
        queueIn: Queue = self.args[0]
        #  queueOut: Queue = self.args[1]
        while True:
            try:
                msg = queueIn.get_nowait()
                queueIn.task_done()
                if msg["cmd"] == "pause":
                    self.player.paused = True
                elif msg["cmd"] == "play":
                    self.player.paused = False
                elif msg["cmd"] == "load":
                    self.player.load(msg["data"])
            except Empty:
                pass
            if self.player.paused:
                #  queueOut.put("paused")
                sleep(0.1)
            else:
                self.player.play()
                #  queueOut.put("playing")
