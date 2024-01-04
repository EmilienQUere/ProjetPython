from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter.simpledialog import askinteger

# Set the background color using RGB values for same backgroung a the picture
rgb_background = (52,73,74) 
background_color = "#{:02x}{:02x}{:02x}".format(*rgb_background)

class AppProd(tk.Tk):
    """ Application GUI in Tkinter"""
    def __init__(self):
        """ Application constructor (inheritance from Tk object)"""
        super().__init__()
        self.screen_h = self.winfo_screenwidth()
        self.screen_v = self.winfo_screenheight()
        self.screen_x = 0
        self.screen_y = 0
        geometry = f"{self.screen_h}x{self.screen_v}+{self.screen_x}+{self.screen_y}"
        self.geometry(geometry)
        self.resizable(True, True)  # (width, height)
        self.minsize(100, 100)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 0.9)  # window transparency
        self.configure(bg="white")

        # Set the window icon
        self.set_icon()
        self.title("Barbak")
        self.init_widgets()

    def set_icon(self):
        """ Set the window icon """
        icon_path = Path("/home/user/Bureau/Projet Python/BARBAK.png")
        try:
            icon_img = Image.open(icon_path)
            icon_img = icon_img.convert("RGBA")
            self.icon_img = ImageTk.PhotoImage(icon_img)
            self.tk.call('wm', 'iconphoto', self._w, self.icon_img)
        except Exception as e:
            print(f"Error setting window icon: {e}")

    def init_widgets(self):
        """ Init all widgets of the main window """
        # Load the image using Pillow
        image_path = "/home/user/Bureau/Projet Python/BARBAK.png"
        try:
            pil_image = Image.open(image_path)
            self.img = ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.img = None

        if self.img:
            # Place the image BARBAK at specific coordinates (x, y)
            self.image = ttk.Label(self, image=self.img)
            self.image.place(x=1680, y=10)

            # Text PRODUCTION
            x_message_position = 1681
            y_message_position = 250
            self.message = ttk.Label(self, text="PRODUCTION", font=("Courier", 20), foreground="White", background=background_color, padding=[32,20])   
            self.message.place(x=x_message_position, y=y_message_position)

            # Bouton Déconnexion
            exit_style = ttk.Style()
            exit_style.configure("Déconnexion.TButton", font=("Courier", 20), foreground="white", background=background_color, padding=[25, 15])

            exit_button = ttk.Button(self, text="Déconnexion", command=self.exit_page, style="Déconnexion.TButton")
            exit_button.place(x=1680, y=800)

            # Tableau des OF's
            columns = ("Produit", "Numéro", "Date", "Quantité à produire")
            self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
 
            style = ttk.Style(self)
            style.configure("Treeview.Heading", font=("Courier", 12), background=background_color, foreground="white")
            style.configure("Treeview", font=("Courier", 10), background="lightGrey")

            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=300, anchor="center",)
                self.tree.place(x=100, y=50)

            # Ajout de quelques données fictives pour l'exemple
            data = [
                ("Produit1", "OF001", "2022-01-10", 100),
                ("Produit2", "OF002", "2022-01-15", 200),
                ("Produit3", "OF003", "2022-01-20", 150),
                ]

            for row in data:
                self.tree.insert("", "end", values=row)
            
            self.tree.bind("<ButtonRelease-1>", self.modify_quantity)

    def exit_page(self):
        """ Exit the page """
        MsgBox = messagebox.askquestion (
            title="Déconnection de l'application", 
            message="Etes vous sûre de vouloir vous déconnecter ? ",
            icon="warning")
        if MsgBox == "yes":
            self.destroy()
    
    def modify_quantity(self, event):
    # Obtenir l'élément sélectionné
        item = self.tree.selection()
        print("true")
        if item:
                # Récupérer la région de l'élément sélectionné
            column_id = self.tree.identify_column(event.x)
            print(column_id)

            # Obtenir l'indice de la colonne à partir de l'identifiant de colonne
            if column_id:
                column_index = self.tree["columns"].index(column_id)
                print(self.tree["columns"])
            
                # Obtenir la valeur de la cellule cliquée
                value = self.tree.item(item, "values")[column_index]
                print(value)


                # Demander à l'utilisateur de modifier la quantité
                #new_quantity = askinteger("Modifier Quantité", f"Modifiez la quantité pour {value} :", initialvalue=int(value))
                #if new_quantity is not None:
                    # Mettre à jour la valeur dans le tableau
                    #self.tree.item(item, values=(self.tree.item(item, 'values')[:3] + (new_quantity,)))


if __name__ == "__main__":
    myApp = AppProd()
    myApp.mainloop()
