import tkinter as tk
from tkinter import ttk

class AppProd(tk.Tk):
    """Application GUI in Tkinter"""
    def __init__(self):
        super().__init__()

    def creer_fenetre_utilisateur(self):
        self.title("Page Production")

        # Modification de la police
        police = ("Helvetica", 12)

        # Cadre principal
        cadre_principal = ttk.Frame(self, padding="20", style="TFrame")
        cadre_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels et entrées
        ttk.Label(cadre_principal, text="Bienvenue sur la page Production", font=police).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="E")

        # Configuration du style
        self.configurer_styles()

        # Configurer la gestion de la redimension de la fenêtre
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Centrer la fenêtre
        self.centrer_fenetre()

    def configurer_styles(self):
        style = ttk.Style()
        # Style pour l'entrée (Entry)
        style.configure("TEntry", padding=(5, 5), relief="flat", background="#f0f0f0")

    def centrer_fenetre(self):
        self.update_idletasks()
        largeur_ecran = self.winfo_screenwidth()
        hauteur_ecran = self.winfo_screenheight()

        largeur_fenetre = self.winfo_reqwidth()
        hauteur_fenetre = self.winfo_reqheight()

        x_position = (largeur_ecran - largeur_fenetre) // 2
        y_position = (hauteur_ecran - hauteur_fenetre) // 2

        self.geometry(f"+{x_position}+{y_position}")

# ================================================================================================

if __name__ == "__main__":
    myApp = AppProd()  # Instance of AppLog
    myApp.creer_fenetre_utilisateur()  # Call the method to create the window
    myApp.mainloop()  # Call mainloop once
