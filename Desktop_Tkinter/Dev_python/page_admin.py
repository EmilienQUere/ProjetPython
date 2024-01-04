from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from test_antonin import AppProd as visuprod

class AppAdmin(tk.Tk):
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

    def exit_page(self):
        """ Exit the page """
        MsgBox = messagebox.askquestion(
            title="Déconnection de l'application",
            message="Etes vous sûre de vouloir vous déconnecter ? ",
            icon="warning")

        if MsgBox == "yes":
           self.destroy()
           self.ouvrir_fenetre_existante()
           


    def onBtnLogin(self):
        """ Callback Btn Login pressed """
        messagebox.showinfo (
        title='Login',
    message=f'Bienvenue {self.user.get()}')

    def ouvrir_fenetre_existante(self):
        fenetre_existante = visuprod()
        fenetre_existante.mainloop()

if __name__ == "__main__":
    myApp = AppAdmin()
    myApp.mainloop()