import tkinter as tk
from tkinter import ttk, messagebox

# Informations sur les utilisateurs
utilisateurs = {
    "utilisateur1": {"mot_de_passe": "motdepasse1", "page": "PageUtilisateur1"},
    "utilisateur2": {"mot_de_passe": "motdepasse2", "page": "PageUtilisateur2"},
    "utilisateur3": {"mot_de_passe": "motdepasse3", "page": "PageUtilisateur3"},
    "utilisateur4": {"mot_de_passe": "motdepasse4", "page": "PageUtilisateur4"},
}

def main():
    creer_fenetre_connexion()

def creer_fenetre_connexion():
    global fenetre_connexion
    fenetre_connexion = tk.Tk()
    fenetre_connexion.title("Page de connexion")

    # Modification de la police
    police = ("Helvetica", 12)

    # Utilisation de StringVar pour stocker la sélection de l'utilisateur
    global nom_utilisateur_var
    nom_utilisateur_var = tk.StringVar()

    # Cadre principal
    cadre_principal = ttk.Frame(fenetre_connexion, padding="20", style="TFrame")
    cadre_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Labels et entrées
    ttk.Label(cadre_principal, text="Nom d'utilisateur:", font=police).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="E")
    ttk.Label(cadre_principal, text="Mot de passe:", font=police).grid(row=1, column=0, padx=(10, 5), pady=5, sticky="E")

    global entry_mot_de_passe
    entry_mot_de_passe = ttk.Entry(cadre_principal, show="*", font=police, style="TEntry")
    entry_mot_de_passe.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="W")

    # Liste déroulante (Combobox) pour choisir l'utilisateur
    global liste_utilisateurs
    liste_utilisateurs = ttk.Combobox(cadre_principal, textvariable=nom_utilisateur_var, values=list(utilisateurs.keys()), font=police)
    liste_utilisateurs.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="W")

    liste_utilisateurs.set(list(utilisateurs.keys())[0])  # Définir la première valeur par défaut

    # Widget œil pour afficher/masquer le mot de passe
    global eye_widget
    eye_widget = EyeWidget(cadre_principal, entry_mot_de_passe)
    eye_widget.grid(row=1, column=2, pady=5, padx=(5, 10), sticky="W")

    # Bouton de connexion
    bouton_connexion = ttk.Button(cadre_principal, text="Se connecter", command=verifier_connexion, style="TButton")
    bouton_connexion.grid(row=3, column=0, columnspan=3, pady=10, sticky="WE")

    # Configuration du style
    configurer_styles()

    # Configurer la gestion de la redimension de la fenêtre
    fenetre_connexion.grid_columnconfigure(0, weight=1)
    fenetre_connexion.grid_rowconfigure(0, weight=1)

    # Centrer la fenêtre
    centrer_fenetre(fenetre_connexion)

    fenetre_connexion.mainloop()

class EyeWidget(tk.Label):
    def __init__(self, parent, target_entry, *args, **kwargs):
        super().__init__(parent, text="👁", font=("Arial", 12), *args, **kwargs)
        self.target_entry = target_entry
        self.eye_state = tk.BooleanVar(value=True)
        self.bind("<Button-1>", self.toggle_eye)

    def toggle_eye(self, event):
        self.eye_state = not self.eye_state.get()
        self.config(text="👁" if self.eye_state else "👁‍🗨")
        self.update_password_visibility()

    def update_password_visibility(self):
        if self.eye_state:
            self.target_entry.config(show="*")
        else:
            self.target_entry.config(show="")

def configurer_styles():
    style = ttk.Style()

    # Style pour l'entrée (Entry)
    style.configure("TEntry", padding=(5, 5), relief="flat", background="#f0f0f0")

    # Style pour le bouton (Button)
    style.configure("TButton", padding=(10, 5), font=("Helvetica", 12, "bold"), foreground="white", background="#4CAF50")

    # Style pour la liste déroulante (Combobox)
    style.configure("TCombobox", padding=(5, 3), font=("Helvetica", 12), background="#f0f0f0")

def verifier_connexion():
    nom_utilisateur = nom_utilisateur_var.get()
    mot_de_passe = entry_mot_de_passe.get()

    if nom_utilisateur in utilisateurs and utilisateurs[nom_utilisateur]["mot_de_passe"] == mot_de_passe:
        page_utilisateur = utilisateurs[nom_utilisateur]["page"]
        ouvrir_page_utilisateur(page_utilisateur)
    else:
        messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

def ouvrir_page_utilisateur(page):
    fenetre_connexion.destroy()  # Fermer la fenêtre de connexion actuelle
    fenetre_utilisateur = tk.Tk()  # Créer une nouvelle fenêtre pour la page de l'utilisateur
    fenetre_utilisateur.title(page)

    # Style personnalisé
    style = ttk.Style()
    style.configure("TFrame", background="#ececec")
    style.configure("TLabel", background="#ececec", font=("Helvetica", 12))
    style.configure("TButton", background="#4CAF50", foreground="white", font=("Helvetica", 12))
    style.configure("TCheckbutton", background="#ececec", font=("Helvetica", 12))

    # Cadre principal
    cadre_principal = ttk.Frame(fenetre_utilisateur, padding="20", style="TFrame")
    cadre_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    label_bienvenue = ttk.Label(cadre_principal, text=f"Bienvenue sur {page}!", style="TLabel")
    label_bienvenue.grid(row=0, column=0, pady=20)

    # Bouton de déconnexion
    bouton_deconnexion = ttk.Button(cadre_principal, text="Déconnexion", command=lambda: deconnexion(fenetre_utilisateur), style="TButton")
    bouton_deconnexion.grid(row=1, column=0, pady=10, sticky="w")

    # Configuration du style pour le cadre principal
    style.configure("TFrame", background="#ececec")

    # Centrer la fenêtre
    centrer_fenetre(fenetre_utilisateur)

    fenetre_utilisateur.mainloop()

def deconnexion(fenetre):
    fenetre.destroy()  # Fermer la fenêtre actuelle
    creer_fenetre_connexion()  # Réafficher la fenêtre de connexion

def centrer_fenetre(fenetre):
    fenetre.update_idletasks()
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()

    largeur_fenetre = fenetre.winfo_reqwidth()
    hauteur_fenetre = fenetre.winfo_reqheight()

    x_position = (largeur_ecran - largeur_fenetre) // 2
    y_position = (hauteur_ecran - hauteur_fenetre) // 2

    fenetre.geometry(f"+{x_position}+{y_position}")

# Fonction principale pour lancer l'application
if __name__ == "__main__":
    main()
