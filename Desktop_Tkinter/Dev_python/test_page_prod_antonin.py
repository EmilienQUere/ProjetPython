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

        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.resizable(True, True)
        self.minsize(100, 100)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 0.9)  # transparence de la fenêtre
        self.configure(bg="white")

        # Définir l'icône de la fenêtre
        self.set_icon()
        self.title("Production Barbak") 
        self.init_widgets()
        self.AffOF()
        self.after(5000, self.actualiser_tableau) 
        
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
        colonnes = ("Produit", "OF", "Date", "Quantité à produire", "Quantité produite", "Etat")
        self.tree = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")

        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Courier", 20), background=background_color, foreground="white")
        style.configure("Treeview", font=("Courier", 15), background="lightGrey", borderwidth=0, highlightthickness=0)

        # Ajuster la hauteur de ligne pour augmenter l'espace entre les lignes
        style.configure("Treeview.Item", font=("Courier", 15), rowheight=30)  # Ajustez la valeur de rowheight selon vos besoins

        for col in colonnes:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=310, anchor="center")

        donnees = []

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

    def actualiser_tableau(self):
        """Actualiser le tableau avec les données les plus récentes."""
        self.AffOF()
        self.after(5000, self.actualiser_tableau)

    def update_table(self, data):
        """Mettre à jour le contenu du tableau avec les nouvelles données."""
        self.tree.delete(*self.tree.get_children())  # Effacer toutes les lignes actuelles

        for ligne in data:
            self.tree.insert("", "end", values=ligne)

    def AffOF(self):
        self.id_of_mapping = {}
        try:
            # Récupérer les OF non terminés et non annulés
            self.of_records = xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw(
                'demo', 2, '2000', 'mrp.production', 'search_read',
                [[('state', 'not in', ['done', 'cancel'])]],
                {'fields': ['product_id', 'name', 'product_qty', 'date_planned_start', 'qty_producing', 'state']}
            )

            # Collecter les données pour mettre à jour le tableau
            table_data = []
            for of in self.of_records:
                article_name = of.get('product_id')[1] if of.get('product_id') else ''
                OF_ID = of.get('id')
                OF_Name = of.get('name')
                Quantity = of.get('product_qty')
                quantity_produced = of.get('qty_producing')
                date = datetime.strptime(of.get('date_planned_start'), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y %H:%M:%S')
                etat_OF = of.get('state')

                table_data.append((article_name, OF_Name, date, Quantity, quantity_produced,etat_OF))   
                self.id_of_mapping[OF_Name] = OF_ID

            # Mettre à jour le tableau avec les nouvelles données
            self.update_table(table_data)

        except Exception as e:
            print(f"Erreur lors de la lecture des ordres de fabrication : {e}")

    def selection_quantite(self, event):
        # Obtenir l'élément sélectionné
        item = self.tree.selection()

        if item and self.modif_en_cours:
            # Récupérer la région de l'élément sélectionné
            colonne = self.tree.identify_column(event.x)
            id_colonne = self.tree.column(colonne)["id"]
            indice_colonne = self.tree["columns"].index(id_colonne)

            # Obtenir la valeur de la cellule à modifier
            values = self.tree.item(item, "values")

            if values:
                # Vérifier si la valeur que vous essayez d'obtenir existe
                OF_Name = values[1]

                # Demander à l'utilisateur de saisir la nouvelle valeur
                nouvelle_valeur = simpledialog.askinteger("Modifier Valeur", f"Modifier la valeur pour l'OF {OF_Name} :", initialvalue=values[4])

                # Obtenir l'ID à partir du dictionnaire
                order_id_to_modify = self.id_of_mapping.get(OF_Name) 

                self.modif_qty(order_id_to_modify, nouvelle_valeur)
                print("ID OF",order_id_to_modify,"new value", nouvelle_valeur)

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
    
    # Fonction pour modifier la quantité produite dans un ordre de fabrication
    def modif_qty(self, order_id, new_quantity):
        try:
            result = xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw(
                'demo', 2, '2000', 'mrp.production', 'write',
                [[order_id], {'qty_producing': new_quantity}]
            )
            if result:
                print(f"Quantité produite dans l'ordre de fabrication avec l'ID {order_id} modifiée avec succès.")
            else:
                print(f"La modification de la quantité produite dans l'ordre de fabrication avec l'ID {order_id} a échoué.")
        except Exception as e:
            print(f"Erreur lors de la modification de la quantité produite : {e}")
    

if __name__ == "__main__":
    monApp = AppProd()
    monApp.mainloop()
