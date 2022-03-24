"""
Front-End.

This code defines the Graphical User Interface class

"""
from tkinter import *
import logging
import tkinter
from tkinter import ttk
from audio_player import Player
from player_logic import player_thread

logger = logging.getLogger(__name__)


class GUI:
    """A simple class
    """

    def __init__(self, name: str) -> None:
        """
        GUI constructor

        :param name: The name of this thing
        :type name: str
        """
        # Create Object, root variable to access Tkinter methods, and define geometry

        self.root = tkinter.Tk()
        self.root.title(name)
        self.root.geometry("300x300+250+100")

        # Global style and Frame definition
        self.style = ttk.Style(self.root)
        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.root.columnconfigure(0, weight=2)
        self.root.rowconfigure(0, weight=2)

        # Jarvis' Switch
        # Keep track of the switch button state on/off
        self.switch_on = False
        self.background_color_index = 00
        self.colors = ["black", "cyan", "lightblue", "olive"]
        self.on_img = PhotoImage(file="../images/on.png")
        self.off_img = PhotoImage(file="../images/off.png")
        self.switch_button = ttk.Button(mainframe, image=self.off_img, command=self.toggle, state=NORMAL)
        self.switch_button.pack(pady=50)

        self.db_data = None
        self.gui_mode = "ready"
        self.p = Player()

    def run(self):
        self.background_color_index = 0
        self.set_background_img(self.colors[self.background_color_index])
        self.root.mainloop()

    def set_background_img(self, color: str):
        """Set the display colour.

        :param color: a colour name or RGB value
        :type color: str
        """
        logger.info(f"color={color}")
        self.style.configure('TFrame', background=color)

    def toggle(self):
        self.background_color_index += 1
        if not self.switch_on:
            self.switch_button.config(image=self.on_img)
            self.background_color_index = 1
            self.switch_on = True
            self.gui_mode = "listening"
            player_thread("Play hello")
        else:
            self.switch_button.config(image=self.off_img)
            self.background_color_index = 0
            self.switch_on = False
            player_thread("Play goodbye")
        self.set_background_img(self.colors[self.background_color_index])


    def gui_mode(self):
        return self.gui_mode

    def listening(self):
        if self.gui_mode == "listening":
            self.switch_button.config(state=DISABLED)
            self.background_color_index = 2
        self.set_background_img(self.colors[self.background_color_index])

    def answer(self):
        if self.gui_mode == "answer":
            self.switch_button.config(state=NORMAL)
            self.background_color_index = 3
        self.set_background_img(self.colors[self.background_color_index])

    def play(self):
        if self.gui_mode == "play":
            self.background_color_index = 4
        self.set_background_img(self.colors[self.background_color_index])

    def after(self):
        self.root.after(self.ms, self.after)
        self.func()

    def set_after(self, ms, func):
        self.root.after(ms, self.after)
        self.ms = ms
        self.func = func

    def state(self):
        return self._state


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    a = GUI("Jarvis")
    a.run()
