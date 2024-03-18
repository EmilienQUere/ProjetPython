import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import xmlrpc.client
import tkinter.simpledialog

COULEUR_DE_FOND = "#{:02x}{:02x}{:02x}".format(52, 73, 74)
image_path = os.path.abspath("BARBAK.png")

#=========================================================================================

class AppProd(tk.Tk):
    """Application GUI en Tkinter"""
    def __init__(self):
        super().__init__()

        # Ajoutez cette ligne pour récupérer le mot de passe du fichier
        self.mdp_to_test = self.load_mdp_to_test()
        self.clear_file()
        self.configurer_fenetre()
        self.title("Production Barbak")
        self.init_widgets()
        self.afficher_OF()
        self.after(5000, self.actualiser_tableau)
        

    def configurer_fenetre(self):
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.resizable(True, True)
        self.minsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 1)
        self.configure(bg="white")
        self.iconphoto(False, tk.PhotoImage(file=image_path))

    def init_widgets(self):
        self.charger_image()
        self.initialiser_bouton_deconnexion()
        self.initialiser_bouton_modifier()
        self.initialiser_tableau()

    def charger_image(self):
        chemin_image = image_path
        try:
            pil_image = Image.open(chemin_image)
            self.image = ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")
            self.image = None

        if self.image:
            x_position, y_position = 10, 650
            self.image_label = ttk.Label(self, image=self.image)
            self.image_label.place(x=x_position, y=y_position)

    def initialiser_bouton_deconnexion(self):
        style_deconnexion = ttk.Style()
        style_deconnexion.configure("Deconnexion.TButton", font=("Courier", 20), foreground="white", background=COULEUR_DE_FOND, padding=[25, 15])

        bouton_deconnexion = ttk.Button(self, text="Déconnexion", command=self.quitter_page, style="Deconnexion.TButton")
        bouton_deconnexion.place(x=1680, y=800)

    def load_mdp_to_test(self):
        # Chargez le mot de passe depuis le fichier
        try:
            with open("test.txt", "r") as file:
                return file.read().strip()            
        except FileNotFoundError:
            return ''
        
    def clear_file(self):
        try:
            os.remove("test.txt")
        except FileNotFoundError:
            print(f"Le fichier n'existe pas.")
        except Exception as e:
            print(f"Erreur fichier : {e}")

    def initialiser_bouton_modifier(self):
        self.modif_en_cours = False

        style_modifier = ttk.Style()
        style_modifier.configure("Modifier.TButton", font=("Courier", 20), foreground="white", background=COULEUR_DE_FOND, padding=[39, 15])

        bouton_modifier = ttk.Button(self, text="Modifier\nquantité", style="Modifier.TButton", command=self.bouton_modifier_clic)
        bouton_modifier.place(x=1680, y=650)

    def initialiser_tableau(self):
        colonnes = ("Produit", "OF", "Date", "Quantité à produire", "Quantité produite", "Etat")
        self.tableau = ttk.Treeview(self, columns=colonnes, show="headings", selectmode="browse")

        self.configurer_styles_tableau(colonnes)
        self.tableau.bind("<ButtonRelease-1>", lambda event: self.selection_quantite(event))
        self.tableau.place(x=40, y=70)

    def configurer_styles_tableau(self, colonnes):
        style = ttk.Style(self)
        style.configure("Treeview.Heading", font=("Courier", 20), background=COULEUR_DE_FOND, foreground="white")
        style.configure("Treeview", font=("Courier", 15), background="lightGrey", borderwidth=0, highlightthickness=0)
        style.configure("Treeview.Item", font=("Courier", 15), rowheight=30)

        for col in colonnes:
            self.tableau.heading(col, text=col)
            self.tableau.column(col, width=310, anchor="center")

    def quitter_page(self):
        MsgBox = messagebox.askquestion(
            title="Déconnexion de l'application",
            message="Êtes-vous sûr de vouloir vous déconnecter ? ",
            icon="warning")
        if MsgBox == "yes":
            self.destroy()
            
    def actualiser_tableau(self):
        self.afficher_OF()
        self.after(500, self.actualiser_tableau)

    def update_table(self, data):
        self.tableau.delete(*self.tableau.get_children())

        for ligne in data:
            self.tableau.insert("", "end", values=ligne)

    def afficher_OF(self):
        self.id_of_mapping = {}
        try:
            self.of_records = xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw(
                'demo2', 9 , self.mdp_to_test , 'mrp.production', 'search_read',
                [[('state', 'not in', ['done', 'cancel', 'to_close'])]],
                {'fields': ['product_id', 'name', 'product_qty', 'date_planned_start', 'qty_producing', 'state']}
            )

            table_data = []
            for of in self.of_records:
                # Ajoutez une condition pour vérifier si l'état de l'OF est "to_close"
                if of.get('state') != 'to_close':
                    article_name = of.get('product_id')[1] if of.get('product_id') else ''
                    OF_ID = of.get('id')
                    OF_Name = of.get('name')
                    Quantity = int(of.get('product_qty'))
                    quantity_produced = int(of.get('qty_producing'))
                    date = datetime.strptime(of.get('date_planned_start'), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y %H:%M:%S')
                    etat_OF = of.get('state')

                    table_data.append((article_name, OF_Name, date, Quantity, quantity_produced, etat_OF))
                    self.id_of_mapping[OF_Name] = OF_ID

            self.update_table(table_data)

        except Exception as e:
            print(f"Erreur lors de la lecture des ordres de fabrication : {e}")
            messagebox.showerror("Erreur de communication", f"Erreur lors de la lecture des ordres de fabrication : {e}, vérifier la connection")

    def selection_quantite(self, event):
        item = self.tableau.selection()

        if item and self.modif_en_cours:
            colonne = self.tableau.identify_column(event.x)
            id_colonne = self.tableau.column(colonne)["id"]
            values = self.tableau.item(item, "values")

            if values:
                OF_Name = values[1]
                nouvelle_valeur = simpledialog.askinteger("Modifier Valeur", f"Modifier la valeur pour l'OF {OF_Name} :", initialvalue=values[4])
                order_id_to_modify = self.id_of_mapping.get(OF_Name)

                self.modif_qty(order_id_to_modify, nouvelle_valeur)

            self.modif_en_cours = False

            style = ttk.Style()
            style.configure("Modifier.TButton", background=COULEUR_DE_FOND)

    def bouton_modifier_clic(self):
        if not self.modif_en_cours:
            self.modif_en_cours = True
            style = ttk.Style()
            style.configure("Modifier.TButton", background="green")
        else:
            self.modif_en_cours = False
            style = ttk.Style()
            style.configure("Modifier.TButton", background=COULEUR_DE_FOND)
    
    def saisir_quantite(self, qty_to_produce):
        while True:
            nouvelle_valeur = tkinter.simpledialog.askinteger("Modifier Valeur", f"La nouvelle quantité produite ne peut pas dépasser {int(qty_to_produce)}. Entrez une nouvelle quantité entière :", initialvalue=int(qty_to_produce))
            if nouvelle_valeur is None:
                return None  # L'utilisateur a appuyé sur Annuler, donc sortez de la boucle
            elif isinstance(nouvelle_valeur, int):
                return nouvelle_valeur  # La valeur est une entière, sortez de la boucle
            else:
                messagebox.showerror("Erreur", "Veuillez entrer une valeur entière.")

    def modif_qty(self, order_id, new_quantity):
        if new_quantity != None :
            try:
                # Récupérez la quantité à produire pour l'OF
                of_record = xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw(
                    'demo2', 9, self.mdp_to_test, 'mrp.production', 'read',
                    [[order_id], ['product_qty']]
                )
                qty_to_produce = of_record[0]['product_qty']

                # Vérifiez si la nouvelle quantité produite est inférieure ou égale à la quantité à produire
                if 0 <= new_quantity <= qty_to_produce:
                    result = xmlrpc.client.ServerProxy(f"{'http://172.31.11.13:8069'}/xmlrpc/2/object").execute_kw(
                        'demo2', 9, self.mdp_to_test, 'mrp.production', 'write',
                        [[order_id], {'qty_producing': new_quantity}]
                    )
                    if result:
                        print(f"Quantité produite dans l'ordre de fabrication avec l'ID {order_id} modifiée avec succès.")
                    else:
                        print(f"La modification de la quantité produite dans l'ordre de fabrication avec l'ID {order_id} a échoué.")
                        messagebox.showerror("Erreur de communication", f"La modification de la quantité produite dans l'ordre de fabrication avec l'ID {order_id} a échoué.")
                else:
                    print(f"La nouvelle quantité produite dépasse la quantité à produire pour l'ordre de fabrication avec l'ID {order_id}.")
                    # Demandez à l'utilisateur de saisir une nouvelle quantité valide
                    nouvelle_quantite = self.saisir_quantite(qty_to_produce)
                    if nouvelle_quantite is not None:
                        # Appelez récursivement modif_qty avec la nouvelle quantité saisie
                        self.modif_qty(order_id, nouvelle_quantite)

            except Exception as e:
                print(f"Erreur lors de la modification de la quantité produite : {e}")
                messagebox.showerror("Erreur de communication", "Erreur lors de la modification de la quantité produite : {e}, vérifier la connection")


#=========================================================================================
            
if __name__ == "__main__":
    monApp = AppProd()
    monApp.mainloop()
