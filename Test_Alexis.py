from pathlib import Path
import tkinter as tk

#============================================================

class App(tk.Tk):
    """Application GUI in TKinter"""
    def __init__(self):
        """Application constructor (heritage=Tk object)"""
        super().__init__()
        self.screen_h = 800
        self.screen_v = self.winfo_screenheight()
        self.screen_x = 50
        self.screen_y = 0
        geometry = str(self.screen_h)+"x"+str(self.screen_v)+"+"+str(self.screen_x)+"+"+str(self.screen_y)

        

#============================================================
        
if __name__ == "__main__":
    myApp = App()
    myApp.mainloop()