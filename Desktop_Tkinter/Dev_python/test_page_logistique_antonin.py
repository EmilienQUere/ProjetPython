import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import xmlrpc.client
import io
import base64

# Définir la couleur de fond en utilisant les valeurs RGB pour le même fond que l'image
rgb_background = (52, 73, 74)
background_color = "#{:02x}{:02x}{:02x}".format(*rgb_background)

class AppLog(tk.Tk):
    """Application GUI en Tkinter"""


    def __init__(self):
        """Constructeur de l'application (héritage de l'objet Tk)"""
        super().__init__()
        self.nom = "Antonin"
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
        self.init_image()
        self.AffichageArticles()
        self.after(5000, self.actualiser_tableau)  # temps en ms

    def set_icon(self):
        """Définir l'icône de la fenêtre"""
        try:
            chemin_icone = "Desktop_Tkinter/Image/BARBAK.png"
            icone_img = Image.open(chemin_icone).convert("RGBA")
            self.icone_img = ImageTk.PhotoImage(icone_img)
            self.tk.call('wm', 'iconphoto', self._w, self.icone_img)
        except Exception as e:
            print(f"Erreur lors du réglage de l'icône de la fenêtre : {e}")

    def init_image(self):
        """Initialiser tous les widgets de la fenêtre principale"""
        # Charger l'image avec Pillow
        image_path = "Desktop_Tkinter/Image/BARBAK.png"
        pil_image = Image.open(image_path)
        self.img = ImageTk.PhotoImage(pil_image)

        # Placer l'image BARBAK à des coordonnées spécifiques (x, y)
        self.image = ttk.Label(self, image=self.img)
        self.image.place(x=10, y=650)

    def init_widgets(self):
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
        bouton_modifier.place(x=1680, y=650)

        # Tableau des articles
        colonnes = ("Nom", "Code", "Prix", "Quantité en stock")
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")

        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Courier", 20), background=background_color, foreground="white")
        style.configure("Treeview", font=("Courier", 15), background="lightGrey", borderwidth=0, highlightthickness=0)

        # Ajuster la hauteur de ligne pour augmenter l'espace entre les lignes
        style.configure("Treeview.Item", font=("Courier", 15), rowheight=30) 

        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=310, anchor="center")

        # Ajout de quelques données fictives pour l'exemple
        donnees = []

        for ligne in donnees:
            self.tree.insert("", "end", values=ligne)

        self.tree.bind("<ButtonRelease-1>", self.selection_quantite)
        self.tree.place(x=100, y=70)

    def quitter_page(self):
        """Quitter la page"""
        MsgBox = messagebox.askquestion(
            title="Déconnexion de l'application",
            message="Êtes-vous sûr de vouloir vous déconnecter ? ",
            icon="warning")
        if MsgBox == "yes":
            self.destroy()

    def actualiser_tableau(self):
        """Actualiser le tableau avec les données les plus récentes."""
        self.AffichageArticles()
        self.after(500, self.actualiser_tableau)

    def update_table(self, data):
        """Mettre à jour le contenu du tableau avec les nouvelles données."""
        self.tree.delete(*self.tree.get_children())  # Effacer toutes les lignes actuelles

        for ligne in data:
            self.tree.insert("", "end", values=ligne)

    def AffichageArticles(self):
        self.id_of_mapping = {}
        try:
            # Récupérer les articles
            self.article_records = xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw(
                'demo2', 2, '2000', 'product.product', 'search_read',
                [[]],
                {'fields': ['name', 'default_code', 'list_price', 'qty_available', 'image_1920']})

            # Collecter les données pour mettre à jour le tableau
            table_data = []
            for article in self.article_records:
                article_ID = article.get('id')
                article_nom = article.get('name')
                Prix_vente = article.get('list_price')
                Cout = article.get('qty_available')
                article_code = article.get('default_code')

                table_data.append((article_nom, article_code, Prix_vente, Cout))
                self.id_of_mapping[article_nom] = article_ID

            image_odoo = article.get('image_1920')
            if image_odoo:
                # Convertir les données binaires de l'image en format image
                image_article = io.BytesIO(base64.b64decode(image_odoo))
                img_article = Image.open(image_article)

                #Taille de l'image
                resized_image_article = img_article.resize((300,300), Image.ANTIALIAS)
                self.img_article = ImageTk.PhotoImage(resized_image_article)

                # Placer l'image 
                self.image_article = ttk.Label(self, image=self.img_article)
                self.image_article.place(x=50, y=500)

            # Mettre à jour le tableau avec les nouvelles données
            self.update_table(table_data)

        except Exception as e:
            print(f"Erreur lors de la récupération et de l'affichage des articles : {e}")

    def selection_quantite(self, event):
        # Obtenir l'élément sélectionné
        item = self.tree.selection()
        print(item)
        if item and self.modif_en_cours:

            # Obtenir la valeur de la cellule à modifier
            values = self.tree.item(item, "values")

            if values:
                # Vérifier si la valeur que vous essayez d'obtenir existe
                article_nom = values[0]

                # Demander à l'utilisateur de saisir la nouvelle valeur
                nouvelle_valeur = simpledialog.askinteger("Modifier Valeur", f"Modifier la valeur pour l'article {article_nom} :", initialvalue=values[3])

                # Obtenir l'ID à partir du dictionnaire
                article_id_to_modify = self.id_of_mapping.get(article_nom) 
                print(article_id_to_modify)


                self.modif_qty(article_id_to_modify, nouvelle_valeur)
                print("ID article",article_id_to_modify,"new value", nouvelle_valeur)

            self.modif_en_cours = False

            style = ttk.Style()
            style.configure("Modifier.TButton", background=background_color)

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

    def modif_qty(self, order_id, new_quantity):
        try:
            result = xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw(
                'demo2', 2, '2000', 'product.product', 'write',
                [[order_id], {'qty_available': new_quantity}]
            )
            if result:
                print(f"Quantité dans le stock de l'article avec l'ID {order_id} modifiée avec succès.")
            else:
                print(f"La modification de la quantité dans le stock de l'article avec l'ID {order_id} a échoué.")
        except Exception as e:
            print(f"Erreur lors de la modification de la quantité dans le stock : {e}")

if __name__ == "__main__":
    monApp = AppLog()
    monApp.mainloop()
