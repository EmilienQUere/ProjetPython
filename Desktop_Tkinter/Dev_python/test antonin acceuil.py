from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from test_page_prod_antonin import AppProd as visuprod

# Set the background color using RGB values for same backgroung a the picture
rgb_background = (52,73,74) 
background_color = "#{:02x}{:02x}{:02x}".format(*rgb_background)

class App(tk.Tk):
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
            x_position = 1680
            y_position = 10
            self.image = ttk.Label(self, image=self.img)
            self.image.place(x=x_position, y=y_position)

            # Text CONNEXION
            x_message_position = 1681
            y_message_position = 250
            self.message = ttk.Label(self, text="CONNEXION", font=("Courier", 20), foreground="White", background=background_color, padding=[40,20])   
            self.message.place(x=x_message_position, y=y_message_position)

            # Bouton Déconnexion
            exit_style = ttk.Style()
            exit_style.configure("Déconnexion.TButton", font=("Courier", 20), foreground="white", background=background_color, padding=[25, 15])

            exit_button = ttk.Button(self, text="Déconnexion", command=self.exit_page, style="Déconnexion.TButton")
            exit_button.place(x=1680, y=800)

            ######################## DIFFERENT SUR CHAQUE PAGE #################################

            self.user = tk.StringVar()
            self.pwd = tk.StringVar()
            self.frmId = ttk.Frame(self)
            self.frmId.pack()
            self.lblUser = ttk.Label(self.frmId, text="Username:")
            self.lblUser.pack()
            self.entUser = ttk.Entry(self.frmId, textvariable=self.user)
            self.entUser.pack()
            self.entUser.focus()
            self.lblPwd = ttk.Label(self.frmId, text="Password:")
            self.lblPwd.pack()
            self.entPwd = ttk.Entry(self.frmId, textvariable=self.pwd, show="*")
            self.entPwd.pack()
            self.btnLogin = ttk.Button(self.frmId, text="Login", command=self.onBtnLogin)
            self.btnLogin.pack()


    def exit_page(self):
        """ Exit the page """
        MsgBox = messagebox.askquestion(
            title="Déconnection de l'application",
            message="Etes vous sûre de vouloir vous déconnecter ? ",
            icon="warning")

        if MsgBox == "yes":
           self.destroy()
           self.ouvrir_fenetre_existante()
           


    def onBtnLogin(self):
        """ Callback Btn Login pressed """
        messagebox.showinfo (
        title='Login',
    message=f'Bienvenue {self.user.get()}')

    def ouvrir_fenetre_existante(self):
        fenetre_existante = visuprod()
        fenetre_existante.mainloop()

if __name__ == "__main__":
    myApp = App()
    myApp.mainloop()