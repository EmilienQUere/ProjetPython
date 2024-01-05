import tkinter as tk
from tkinter import ttk

class AppLog(tk.Tk): # objet AppLog
    def __init__(self):
        self.fenetre_utilisateur = (tk.Tk)
        

    def creer_fenetre_utilisateur(self): # methode
        self.fenetre_utilisateur.title("Page logistique")
        # Modification de la police
        police = ("Helvetica", 12)

        # Cadre principal
        cadre_principal = ttk.Frame(self.fenetre_utilisateur, padding="20", style="TFrame")
        cadre_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels et entrées
        ttk.Label(cadre_principal, text="Bienvenue sur la page Logistique", font=police).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="E")

        # Configuration du style
        self.configurer_styles() # acces a une methode

        # Configurer la gestion de la redimension de la fenêtre
        self.fenetre_utilisateur.grid_columnconfigure(0, weight=1) # acces attribut
        self.fenetre_utilisateur.grid_rowconfigure(0, weight=1)

        # Centrer la fenêtre
        self.centrer_fenetre(self.fenetre_utilisateur)

        self.fenetre_utilisateur.mainloop()

    def configurer_styles(self):
            style = ttk.Style()
            # Style pour l'entrée (Entry)
            style.configure("TEntry", padding=(5, 5), relief="flat", background="#f0f0f0")

    def centrer_fenetre(self, fenetre):
            self.fenetre_utilisateur.update_idletasks()
            largeur_ecran = self.fenetre_utilisateur.winfo_screenwidth()
            hauteur_ecran = self.fenetre_utilisateur.winfo_screenheight()

            largeur_fenetre = self.fenetre_utilisateur.winfo_reqwidth()
            hauteur_fenetre = self.fenetre_utilisateur.winfo_reqheight()

            x_position = (largeur_ecran - largeur_fenetre) // 2
            y_position = (hauteur_ecran - hauteur_fenetre) // 2

            self.fenetre_utilisateur.geometry(f"+{x_position}+{y_position}")

#================================================================================================
            
if __name__ == "__main__":
    myApp = AppLog() # instance oblet AppLog
    myApp.mainloop()