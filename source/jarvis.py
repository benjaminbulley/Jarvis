from tkinter import *

"""
Front-End.

This code defines the Graphical User Interface class

"""

import logging
import tkinter
from tkinter import ttk

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

        # Global style
        self.style = ttk.Style(self.root)
        # Frame definition
        mainframe = ttk.Frame(self.root)
        mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.root.columnconfigure(0, weight=2)
        self.root.rowconfigure(0, weight=2)

        # Jarvis' Switch
        # Keep track of the switch button state on/off
        self.switch_button_text = tkinter.StringVar(value='Switch')
        self.switch_button = ttk.Button(mainframe, textvariable=self.switch_button_text, command=self.click)
        self.switch_on = True
        self.idx = 00
        self.colors = ["black", "cyan", "lightblue", "olive"]
        self.on_img = PhotoImage(file="../images/on.png")
        self.off_img = PhotoImage(file="../images/off.png")
        self.switch_button.grid(column=1, row=2, columnspan=2, rowspan=2)
        self.switch_button = ttk.Button(
            mainframe,
            image=self.on_img,
            textvariable=self.switch_button_text,
            command=self.switch
        )

        # Mic On/off Button
        self.mic_on = True
        self.mic_on_off_button_text = tkinter.StringVar(value='Mic On')
        self.mic_on_off_button = ttk.Button(mainframe, textvariable=self.mic_on_off_button_text, command=self.click)
        self.mic_on_off_button.grid(column=1, row=2, columnspan=2, rowspan=2)
        self.style.configure('TButton', background='lightblue')
        self.style.configure('TFrame', background=self.colors[0])

        # Define mic on_img/off button
        self.mic_on_off_button = ttk.Button(
            mainframe,
            image=self.on_img,
            textvariable=self.mic_on_off_button_text,
            command=self.switch
        )

    def run(self, a: str):
        """[summary]

        Args:
            a (str): [description]
        """
        self.root.mainloop()

    def set_background(self, color: str):
        """Set the display colour.

        :param color: a colour name or RGB value
        :type color: str
        """
        logger.info(f"color={color}")
        self.style.configure('TFrame', background=color)

    def click(self):
        """Called when mic_on_off_button clicked.
        """
        logger.info("click")
        self.click_action()

    def click_action(self):
        """An example action to use with click()
        """
        self.idx += 1
        if self.idx == len(self.colors):
            self.idx = 0
        self.set_background(self.colors[self.idx])

    def switch(self):
        if self.switch_on:
            self.switch_button.config(image=self.off_img)
            self.idx += 1

        else:
            self.idx = len(self.colors)
            self.switch_button.config(image=self.on_img)
            self.set_background(self.colors[self.idx])
            self.switch_on = True


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    a = GUI("Jarvis")
    a.run("go")
