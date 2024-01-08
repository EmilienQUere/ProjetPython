import tkinter as tk
from tkinter import ttk, messagebox
import xmlrpc.client
from page_admin import AppAdmin as visuAdmin
from page_logistique import AppLog as visuLog
from page_production import AppProd as visuprod

# Informations sur les utilisateurs
utilisateurs = {"administrateur", "production", "logistique", "vente"}

# Variable globale
fenetre_connexion = None
nom_utilisateur_var = None
entry_mot_de_passe = None


#======================================================================================================================================================================

def creer_fenetre_connexion(fenetre_connexion):

    fenetre_connexion.title("Barbak SARL")

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
    liste_utilisateurs = ttk.Combobox(cadre_principal, textvariable=nom_utilisateur_var, values=list(utilisateurs), font=police)
    liste_utilisateurs.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="W")

    liste_utilisateurs.set(list(utilisateurs)[0])  # Définir la première valeur par défaut

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

#======================================================================================================================================================================

def configurer_styles():
    style = ttk.Style()

    # Style pour l'entrée (Entry)
    style.configure("TEntry", padding=(5, 5), relief="flat", background="#f0f0f0")

    # Style pour le bouton (Button)
    style.configure("TButton", padding=(10, 5), font=("Helvetica", 12, "bold"), foreground="white", background="#4CAF50")

    # Style pour la liste déroulante (Combobox)
    style.configure("TCombobox", padding=(5, 3), font=("Helvetica", 12), background="#f0f0f0")
    
#======================================================================================================================================================================

def verifier_connexion():
    global nom_utilisateur_var
    global entry_mot_de_passe
    nom_utilisateur = nom_utilisateur_var.get()
    mot_de_passe = entry_mot_de_passe.get()
    
    connect(nom_utilisateur, mot_de_passe)

    odoo_models, odoo_connection = connect(nom_utilisateur, mot_de_passe)
    if odoo_connection and odoo_models:
        print("Connexion réussie à Odoo")
        ouvrir_page_utilisateur(nom_utilisateur)
    else:
        print("Échec de connexion à Odoo")
        messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

#======================================================================================================================================================================

def connect(nom_utilisateur,mot_de_passe):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format('http://172.31.11.13:8069'))
        uid = common.authenticate('demo', nom_utilisateur, mot_de_passe, {})
        
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format('http://172.31.11.13:8069'))
            return models, xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format('http://172.31.11.13:8069'))
        else:
            print("Connexion échouée : Authentification impossible")
            return None, None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None, None

#======================================================================================================================================================================

def ouvrir_page_utilisateur(nom_utilisateur):

    fenetre_connexion.destroy()  # Fermer la fenêtre de connexion actuelle

# Ouvrir une nouvelle page administrateur

    if nom_utilisateur == "administrateur":
        fenetre_utilisateur = visuAdmin()
        
# Ouvrir une nouvelle page logistique
        
    elif nom_utilisateur == "logistique":
        fenetre_utilisateur = visuLog() 
        
# Ouvrir une nouvelle page production
        
    elif nom_utilisateur == "production":
        fenetre_utilisateur = visuprod() 
    
    fenetre_utilisateur.creer_fenetre_utilisateur()
    fenetre_utilisateur.mainloop()

#======================================================================================================================================================================

#def deconnexion(fenetre):
#    fenetre.destroy()  # Fermer la fenêtre actuelle
#    creer_fenetre_connexion()  # Réafficher la fenêtre de connexion

#======================================================================================================================================================================

def centrer_fenetre(fenetre):
    fenetre.update_idletasks()
    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()

    largeur_fenetre = fenetre.winfo_reqwidth()
    hauteur_fenetre = fenetre.winfo_reqheight()

    x_position = (largeur_ecran - largeur_fenetre) // 2
    y_position = (hauteur_ecran - hauteur_fenetre) // 2

    fenetre.geometry(f"+{x_position}+{y_position}")

#======================================================================================================================================================================

# Fonction principale pour lancer l'application
if __name__ == "__main__":
    fenetre_connexion = tk.Tk()
    creer_fenetre_connexion(fenetre_connexion)
