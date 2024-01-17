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
        self.minsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 0.9)  # transparence de la fenêtre
        self.configure(bg="white")
        self.iconphoto(False, tk.PhotoImage(file="Desktop_Tkinter/Image/BARBAK.png"))

        self.selected_product_image = None

        
        self.title("Barbak")
        self.init_widgets()
        self.init_image()
        self.AffichageArticles()
        self.after(5000, self.actualiser_tableau)  # temps en ms

    def init_widgets(self):
        # Bouton Déconnexion
        self.init_exit_button()
        self.init_modify_button()
        self.init_table()

    def init_image(self):
        """Initialiser tous les widgets de la fenêtre principale"""
        # Charger l'image avec Pillow
        image_path = "Desktop_Tkinter/Image/BARBAK.png"
        pil_image = Image.open(image_path)
        self.img = ImageTk.PhotoImage(pil_image)

        # Placer l'image BARBAK à des coordonnées spécifiques (x, y)
        self.image = ttk.Label(self, image=self.img)
        self.image.place(x=10, y=650)

        # Créer un widget Label pour afficher l'image du produit sélectionné
        self.selected_product_image_label = ttk.Label(self, image=None)
        self.selected_product_image_label.place(x=1000, y=500)

    def init_exit_button(self):
        exit_style = ttk.Style()
        exit_style.configure("Déconnexion.TButton", font=("Courier", 20), foreground="white", background=background_color, padding=[25, 15])

        exit_button = ttk.Button(self, text="Déconnexion", command=self.quitter_page, style="Déconnexion.TButton")
        exit_button.place(x=1680, y=800)

    def init_modify_button(self):
        self.modif_en_cours = False

        style_modifier = ttk.Style()
        style_modifier.configure("Modifier.TButton", font=("Courier", 20), foreground="white", background=background_color, padding=[39, 15])

        bouton_modifier = ttk.Button(self, text="Modifier\nquantité", style="Modifier.TButton", command=self.bouton_modifier_clic)
        bouton_modifier.place(x=1680, y=650)

    def init_table(self):
        colonnes = ("Nom", "Code", "Prix en € (Kg)", "Quantité en stock")
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")

        self.configure_tree_styles()

        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=310, anchor="center")

        self.tree.bind("<ButtonRelease-1>", self.selection_quantite)
        self.tree.place(x=100, y=70)

    def configure_tree_styles(self):
        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Courier", 20), background=background_color, foreground="white")
        style.configure("Treeview", font=("Courier", 15), background="lightGrey", borderwidth=0, highlightthickness=0)

        # Ajuster la hauteur de ligne pour augmenter l'espace entre les lignes
        style.configure("Treeview.Item", font=("Courier", 15), rowheight=30)

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
        ##self.update_table(self)
        self.after(5000, self.actualiser_tableau)

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
                'demo2','2','2000','product.product', 'search_read',
                [[]],
                {'fields': ['name', 'default_code', 'list_price', 'qty_available', 'image_1920']})

            # Collecter les données pour mettre à jour le tableau
            table_data = []
            for article in self.article_records:
                article_ID = article.get('id')
                article_nom = article.get('name')
                prix_vente = round(article.get('list_price'), 2) if article.get('list_price') else 'Non renseigné'
                quantité_stock = int(article.get('qty_available')) if article.get('qty_available') else '0'
                article_code = article.get('default_code') if article.get('default_code') else 'Non renseigné'

                table_data.append((article_nom, article_code, prix_vente, quantité_stock))
                self.id_of_mapping[article_nom] = article_ID

            # Mettre à jour le tableau avec les nouvelles données
            self.update_table(table_data)

        except Exception as e:
            print(f"Erreur lors de la récupération et de l'affichage des articles : {e}")

    def selection_quantite(self, event):
        # Obtenir l'élément sélectionné
        item = self.tree.selection()

        # Obtenir la valeur de la cellule à modifier
        values = self.tree.item(item, "values")

        # Même si values n'est pas défini, essayez d'obtenir article_nom pour la mise à jour de l'image
        if values:
            self.article_nom = values[0]
            self.current_selected_product = self.article_nom
            self.update_selected_product_image()

        if item and self.modif_en_cours and values:
            # Vérifier si la valeur que vous essayez d'obtenir existe
            article_nom = values[0]

            # Demander à l'utilisateur de saisir la nouvelle valeur
            nouvelle_valeur = simpledialog.askinteger("Modifier Valeur", f"Modifier la valeur pour l'article {article_nom} :", initialvalue=values[3])

            # Obtenir l'ID à partir du dictionnaire
            article_id_to_modify = self.id_of_mapping.get(article_nom)

            self.modif_qty(article_id_to_modify, nouvelle_valeur)

        self.modif_en_cours = False
        self.configure_modify_button()

    def update_selected_product_image(self):
        # Mettre à jour l'image du produit sélectionné dans le Label
        if self.current_selected_product:
            selected_product_image = self.get_selected_product_image(self.current_selected_product)
            self.selected_product_image_label.configure(image=selected_product_image)
            self.selected_product_image_label.image = selected_product_image

    def get_selected_product_image(self, article_nom):
        # Récupérer l'enregistrement du produit
        selected_product = next((article for article in self.article_records if article['name'] == article_nom), None)

        if selected_product:
            # Récupérer l'image du produit
            image_odoo = selected_product.get('image_1920')

            if image_odoo:
                # Convertir les données binaires de l'image en format image
                image_article = io.BytesIO(base64.b64decode(image_odoo))
                img_article = Image.open(image_article)
                resized_image_article = img_article.resize((300, 300), Image.LANCZOS)
                selected_product_image = ImageTk.PhotoImage(resized_image_article)

                return selected_product_image

        return None

    def bouton_modifier_clic(self):
        self.modif_en_cours = not self.modif_en_cours
        self.configure_modify_button()
        print("True" if self.modif_en_cours else "False")

    def configure_modify_button(self):
        style = ttk.Style()
        button_color = "green" if self.modif_en_cours else background_color
        style.configure("Modifier.TButton", background=button_color)

    def modif_qty(self, product_id, new_quantity):

        try:
            # Modifie la quantité disponible (qty_available) dans le stock.quant
            stock_quant_ids = xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw('demo2', 2, '2000', 'stock.quant', 'search',
                [[('product_id', '=', product_id)]]
            )
            if stock_quant_ids:
                xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw('demo2', '2', '2000', 'stock.quant', 'write',
                    [stock_quant_ids, {'quantity': new_quantity}]
                )
                print(f"Quantité dans le stock de l'article avec l'ID {product_id} modifiée avec succès.")
            else:
                print(f"Aucun enregistrement stock.quant trouvé pour le produit avec l'ID {product_id}.")

        except Exception as e:
            print(f"Erreur lors de la modification de la quantité dans le stock : {e}")

if __name__ == "__main__":
    monApp = AppLog()
    monApp.mainloop()
