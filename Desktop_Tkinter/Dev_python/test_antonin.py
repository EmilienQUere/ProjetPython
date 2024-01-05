from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
# Définir la couleur de fond en utilisant les valeurs RGB pour le même fond que l'image
rgb_background = (52, 73, 74)
background_color = "#{:02x}{:02x}{:02x}".format(*rgb_background)

class AppProd(tk.Tk):
    """Application GUI en Tkinter"""
    def __init__(self):
        """Constructeur de l'application (héritage de l'objet Tk)"""
        super().__init__()
        self.screen_h = self.winfo_screenwidth()
        self.screen_v = self.winfo_screenheight()
        self.screen_x = 0
        self.screen_y = 0
        geometry = f"{self.screen_h}x{self.screen_v}+{self.screen_x}+{self.screen_y}"
        self.geometry(geometry)
        self.resizable(True, True)  # (largeur, hauteur)
        self.minsize(100, 100)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 0.9)  # transparence de la fenêtre
        self.configure(bg="white")

        # Définir l'icône de la fenêtre
        self.set_icon()
        self.title("Barbak")
        self.init_widgets()

    def set_icon(self):
        """Définir l'icône de la fenêtre"""
        chemin_icone = Path("/home/user/Bureau/Projet Python/BARBAK.png")
        try:
            icone_img = Image.open(chemin_icone)
            icone_img = icone_img.convert("RGBA")
            self.icone_img = ImageTk.PhotoImage(icone_img)
            self.tk.call('wm', 'iconphoto', self._w, self.icone_img)
        except Exception as e:
            print(f"Erreur lors du réglage de l'icône de la fenêtre : {e}")

    def init_widgets(self):
        """Initialiser tous les widgets de la fenêtre principale"""
        # ... (code précédent)

        # Bouton modifier
        #style_modifier = ttk.Style()
        #style_modifier.configure("Modifier.TButton", font=("Courier", 20), foreground="white", background=background_color, padding=[25, 15])

        #bouton_modifier = ttk.Button(self, text="Modifier", command=self.clic_bouton_modifier, style="Modifier.TButton")
        #bouton_modifier.place(x=1680, y=500)

        # Tableau des OF's
        colonnes = ("Produit", "Numéro", "Date", "Quantité à produire", "Quantité produite")
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")

        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Courier", 12), background=background_color, foreground="white")
        style.configure("Treeview", font=("Courier", 10), background="lightGrey")

        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300, anchor="center",)
            self.tree.place(x=100, y=50)

        # Ajout de quelques données fictives pour l'exemple
        donnees = [
            ("Produit1", "OF001", "2022-01-10", 100, 50),
            ("Produit2", "OF002", "2022-01-15", 200, 100),
            ("Produit3", "OF003", "2022-01-20", 150, 120),
        ]

        for ligne in donnees:
            self.tree.insert("", "end", values=ligne)

        self.tree.bind("<ButtonRelease-1>", self.selection_quantite)

    def quitter_page(self):
        """Quitter la page"""
        MsgBox = messagebox.askquestion (
            title="Déconnexion de l'application", 
            message="Êtes-vous sûr de vouloir vous déconnecter ? ",
            icon="warning")
        if MsgBox == "yes":
            self.destroy()

    def selection_quantite(self, event):
        # Obtenir l'élément sélectionné
        item = self.tree.selection()

        if item:
            # Récupérer la région de l'élément sélectionné
            colonne = self.tree.identify_column(event.x)
            id_colonne = self.tree.column(colonne)["id"]
            indice_colonne = self.tree["columns"].index(id_colonne)

            # Obtenir la valeur de la cellule à modifier
            numero_of = self.tree.item(item, "values")[1]
            quantite_a_modifier = self.tree.item(item, "values")[4]
            print(numero_of, quantite_a_modifier)

            # Demander à l'utilisateur de saisir la nouvelle valeur
            nouvelle_valeur = simpledialog.askinteger("Modifier Valeur", f"Modifier la valeur pour l'OF {numero_of} :", initialvalue=quantite_a_modifier)
            
            # Mettre à jour la valeur dans le tableau
            if nouvelle_valeur is not None:
                valeurs = list(self.tree.item(item, 'values'))
                valeurs[indice_colonne] = nouvelle_valeur
                self.tree.item(item, values=valeurs)

if __name__ == "__main__":
    monApp = AppProd()
    monApp.mainloop()
