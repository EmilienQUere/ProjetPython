from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class AppProd(tk.Tk):
    """ Application GUI in Tkinter"""
    def __init__(self):
        """ Application constructor (inheritance from Tk object)"""
        super().__init__()
        self.screen_h = self.winfo_screenwidth()
        self.screen_v = self.winfo_screenheight()
        self.screen_x = 0
        self.screen_y = 0
        geometry = f"{self.screen_h}x{self.screen_v}+{self.screen_x}+{self.screen_y}"
        self.geometry(geometry)
        self.resizable(True, True)  # (width, height)
        self.minsize(100, 100)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 0.9)  # window transparency

if __name__ == "__main__":
    myApp = AppProd()
    myApp.mainloop()