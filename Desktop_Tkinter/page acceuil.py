import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

# Informations sur les utilisateurs
utilisateurs = {
    "Administrateur": {"mot_de_passe": "1111", "page": "Admin"},
    "Production": {"mot_de_passe": "2222", "page": "Production"},
    "Logistique": {"mot_de_passe": "3333", "page": "Logistique"},
    "Vente": {"mot_de_passe": "4444", "page": "Vente"},
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

    #Logo et titre de la fenetre
    fenetre_connexion.title("Barbak SARL")
    chemin_icone = (Path("Viande.ico"))
    #fenetre_connexion.iconbitmap(chemin_icone)

    fenetre_connexion.mainloop()

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

  # Dimenssionnement de la fenetre
    fenetre_utilisateur.screen_h = fenetre_utilisateur.winfo_screenwidth()
    fenetre_utilisateur.screen_v = fenetre_utilisateur.winfo_screenheight()
    fenetre_utilisateur.screen_x = 0
    fenetre_utilisateur.screen_y = 0
    geometry = str(fenetre_utilisateur.screen_h)+"x"+str(fenetre_utilisateur.screen_v)+"+"+str(fenetre_utilisateur.screen_x)+"+"+str(fenetre_utilisateur.screen_y)
    fenetre_utilisateur.geometry(geometry)
    fenetre_utilisateur.resizable(True, True) # (width, heigth)
    fenetre_utilisateur.minsize(100, 100)
    fenetre_utilisateur.maxsize(fenetre_utilisateur.winfo_screenwidth(), fenetre_utilisateur.winfo_screenheight())
    fenetre_utilisateur.attributes('-alpha', 0.9) # window transparency

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
    label_bienvenue.grid(row=700, column=700, pady=20)

    # Bouton de déconnexion
    bouton_deconnexion = ttk.Button(cadre_principal, text="Déconnexion", command=lambda: deconnexion(fenetre_utilisateur), style="TButton")
    bouton_deconnexion.grid(row=1, column=0, pady=10, sticky="w")

    # Configuration du style pour le cadre principal
    style.configure("TFrame", background="#ececec")
  
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
