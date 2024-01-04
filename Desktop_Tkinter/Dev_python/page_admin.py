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

def creer_fenetre_utilisateur():
    global fenetre_utilisateur
    fenetre_utilisateur = tk.Tk()
    fenetre_utilisateur.title("Page Admin")

    # Modification de la police
    police = ("Helvetica", 12)

    # Cadre principal
    cadre_principal = ttk.Frame(fenetre_utilisateur, padding="20", style="TFrame")
    cadre_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Labels et entrées
    ttk.Label(cadre_principal, text="Bienvenue sur la page Production", font=police).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="E")

    # Configuration du style
    configurer_styles()

    # Configurer la gestion de la redimension de la fenêtre
    fenetre_utilisateur.grid_columnconfigure(0, weight=1)
    fenetre_utilisateur.grid_rowconfigure(0, weight=1)

    # Centrer la fenêtre
    centrer_fenetre(fenetre_utilisateur)

    fenetre_utilisateur.mainloop()

def configurer_styles():
    style = ttk.Style()

    # Style pour l'entrée (Entry)
    style.configure("TEntry", padding=(5, 5), relief="flat", background="#f0f0f0")

    # Style pour le bouton (Button)
    style.configure("TButton", padding=(10, 5), font=("Helvetica", 12, "bold"), foreground="white", background="#4CAF50")

    # Style pour la liste déroulante (Combobox)
    style.configure("TCombobox", padding=(5, 3), font=("Helvetica", 12), background="#f0f0f0")

def centrer_fenetre(fenetre):
    fenetre.update_idletasks()
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()

    largeur_fenetre = fenetre.winfo_reqwidth()
    hauteur_fenetre = fenetre.winfo_reqheight()

    x_position = (largeur_ecran - largeur_fenetre) // 2
    y_position = (hauteur_ecran - hauteur_fenetre) // 2

    fenetre.geometry(f"+{x_position}+{y_position}")

if __name__ == "__main__":
    myApp = AppAdmin()
    myApp.mainloop()