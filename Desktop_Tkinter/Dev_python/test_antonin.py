from pathlib import Path
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk

class Page_Tkinter():
    def __init__(self):
        self.root = tk.Tk()

    def charger_image(self, image_path):
        try:
            pil_image = Image.open(image_path)
            self.img = ImageTk.PhotoImage(pil_image)
            print("Image chargée")
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")
            self.img = None

    # Utilisez la méthode charger_image à l'intérieur de votre instance de classe
    def charger_image_instance(self):
        image_path = "/home/user/Bureau/Projet Python/BARBAK.png"
        self.charger_image(image_path)

# Créez une instance de la classe et appelez la fonction
page = Page_Tkinter()
page.charger_image_instance()
page.root.mainloop()
