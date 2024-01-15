from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import sys
sys.path.append("/home/user/Bureau/Projet Python/ProjetPython/ODOO/Dev_python/Lecture_OF.py")

# Définir la couleur de fond en utilisant les valeurs RGB pour le même fond que l'image
rgb_background = (52, 73, 74)
background_color = "#{:02x}{:02x}{:02x}".format(*rgb_background)

class AppProd(tk.Tk):
    """Application GUI en Tkinter"""

    def __init__(self):
        """Constructeur de l'application (héritage de l'objet Tk)"""
        super().__init__()

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.resizable(True, True)
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
        chemin_icone = Path("Desktop_Tkinter/Image/BARBAK.png")
        try:
            icone_img = Image.open(chemin_icone)
            icone_img = icone_img.convert("RGBA")
            self.icone_img = ImageTk.PhotoImage(icone_img)
            self.tk.call('wm', 'iconphoto', self._w, self.icone_img)
        except Exception as e:
            print(f"Erreur lors du réglage de l'icône de la fenêtre : {e}")

    def init_widgets(self):
        """Initialiser tous les widgets de la fenêtre principale"""
        # Load the image using Pillow
        image_path = "Desktop_Tkinter/Image/BARBAK.png"
        try:
            pil_image = Image.open(image_path)
            self.img = ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.img = None

        if self.img:
            # Place the image BARBAK at specific coordinates (x, y)
            x_position = 1680
            y_position = 10
            self.image = ttk.Label(self, image=self.img)
            self.image.place(x=x_position, y=y_position)

        # Bouton Déconnexion
        exit_style = ttk.Style()
        exit_style.configure("Déconnexion.TButton", font=("Courier", 20), foreground="white", background=background_color, padding=[25, 15])

        exit_button = ttk.Button(self, text="Déconnexion", command=self.quitter_page, style="Déconnexion.TButton")
        exit_button.place(x=1680, y=800)

        # Bouton modifier
        self.modif_en_cours = False

        style_modifier = ttk.Style()
        style_modifier.configure("Modifier.TButton", font=("Courier", 20), foreground="white", background=background_color, padding=[39, 15])

        bouton_modifier = ttk.Button(self, text="Modifier\nquantité", style="Modifier.TButton", command=self.bouton_modifier_clic)
        bouton_modifier.place(x=1680, y=300)

        # Tableau des OF's
        colonnes = ("Produit", "Numéro", "Date", "Quantité à produire", "Quantité produite")
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")

        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Courier", 20), background=background_color, foreground="white")
        style.configure("Treeview", font=("Courier", 15), background="lightGrey", borderwidth=0, highlightthickness=0)

        # Ajuster la hauteur de ligne pour augmenter l'espace entre les lignes
        style.configure("Treeview.Item", font=("Courier", 15), rowheight=30)  # Ajustez la valeur de rowheight selon vos besoins

        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=310, anchor="center")

        #####################################################
        # TODO reprendre les donnee produit via programme emilien 
        ##################################################### 

        # Ajout de quelques données fictives pour l'exemple
        donnees = [
            ("Produit1", "OF001", "2022-01-10", 100, 50),
            ("Produit2", "OF002", "2022-01-15", 200, 100),
            ("Produit3", "OF003", "2022-01-20", 150, 120),
        ]

        for ligne in donnees:
            self.tree.insert("", "end", values=ligne)

        self.tree.bind("<ButtonRelease-1>", self.selection_quantite)
        self.tree.place(x=100, y=50)

    def quitter_page(self):
        """Quitter la page"""
        MsgBox = messagebox.askquestion(
            title="Déconnexion de l'application",
            message="Êtes-vous sûr de vouloir vous déconnecter ? ",
            icon="warning")
        if MsgBox == "yes":
            self.destroy()

    def selection_quantite(self, event):
        # Obtenir l'élément sélectionné
        item = self.tree.selection()

        if item and self.modif_en_cours:
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

            #####################################################
            # TODO renvoyer nouvelle valeur via programme emilien 
            ##################################################### 

            self.modif_en_cours = False

            style = ttk.Style()
            style.configure("Modifier.TButton", background=background_color)

    # Couleur et retour bouton modification d'OF
    def bouton_modifier_clic(self):
        if self.modif_en_cours == False:
            self.modif_en_cours = True
            style = ttk.Style()
            style.configure("Modifier.TButton", background="green")
            print("True")
        else : 
            print("faux")
            self.modif_en_cours = False
            style = ttk.Style()
            style.configure("Modifier.TButton", background=background_color)


if __name__ == "__main__":
    monApp = AppProd()
    monApp.mainloop()
