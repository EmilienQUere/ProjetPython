import tkinter as tk
from tkinter import ttk, messagebox, Tk, Frame
from PIL import ImageTk, Image
import xmlrpc.client
from Page_Logistique import AppLog as visuLog
from Page_Production import AppProd as visuprod


bg_color = "#f1f1f1"
txt_color = "#34494A"


class App(tk.Tk):
    """ Application GUI in TKinter"""
    def __init__(self):
        
        """ Application constructor (heritage=Tk object)"""
        super().__init__()
        self.screen_h = 500     #self.winfo_screenwidth()    pour prendre toute la taille de la fenetre
        self.screen_v = 650     #self.winfo_screenheight()
        self.screen_x = int((self.winfo_screenwidth()/2) - (self.screen_h/2))   #centrer la fenetre
        self.screen_y = 0       #self.winfo_height/2
        geometry = str(self.screen_h)+"x"+str(self.screen_v)+"+"+str(self.screen_x)+"+"+str(self.screen_y)
        self.geometry(geometry)
        self.resizable(True, True) #(width, height)
        self.minsize(380, 550)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 0.9)
        self.config(bg=bg_color)
        self.iconphoto(False, tk.PhotoImage(file="Desktop_Tkinter/Image/BARBAK.png"))
        self.title("Login Barbak")

        """Appel des fonctions"""
        self.frame()
        self.widget_texte()
        self.widget_image()
        self.user()
        self.mot_de_passe()
        self.bouton_connexion()
        self.bouton_quitter()

    def frame(self):

        self.middle_frame = Frame(self, width=250, height=500, bg=bg_color)
        self.middle_frame.pack(side="top")

        self.log_frame = Frame(self.middle_frame, width=250, height=600, bg=bg_color)
        self.log_frame.pack(side="bottom", pady=20)

        self.connexion_frame = Frame(self, width=250, height=500, bg=bg_color)
        self.connexion_frame.pack()

        self.quitter_frame = Frame(self, width=100, height=125, bg=bg_color)
        self.quitter_frame.pack(side="bottom", anchor="e")

    def widget_texte(self):    
        self.message = ttk.Label(self.middle_frame, text="Login",font=("Helvetica", 50),foreground=txt_color, background=bg_color)
        self.message.pack(ipady=20) #ipady pour definir le  nombre de pixel en y a ajouter en dessous et au dessus du texte

    def widget_image(self):

        #Ouvrir image
        mon_image = Image.open("Desktop_Tkinter/Image/BARBAK.png")
        #print(mon_image.size)  #taille par défaut de l'image

        #Redimensionner image
        resized_image = mon_image.resize((225,225), Image.LANCZOS)
        self.new_image = ImageTk.PhotoImage(resized_image)
        
        #Placer image
        self.image = ttk.Label(self.middle_frame, image=self.new_image)
        self.image.pack()    #use anchor = 'ne' pour placer l'image en haut à droite

    def user(self):
        utilisateurs = { "Production", "Logistique"}

        self.user = ttk.Label(self.log_frame, text="Nom d'utilisateur",font=("Helvetica", 13),foreground=txt_color, background=bg_color)
        self.user.grid(row=0, column=0, pady=10, ipadx=5, ipady=5)
        
        self.user_list = ttk.Combobox(self.log_frame,values=list(utilisateurs), font=("Helvetica", 13),foreground="black", background="white")
        self.user_list.grid(row=0, column=1, pady=2, ipady=2)
        self.user_list.set(list(utilisateurs)[0])

    def mot_de_passe(self):

        self.mdp = ttk.Label(self.log_frame, text="Mot de passe",font=("Helvetica", 13),foreground=txt_color, background=bg_color)
        self.mdp.grid(row=1, column=0, pady=10, ipadx=5, ipady=5)

        self.mdp_entry = ttk.Entry(self.log_frame, show="*",font=("Helvetica", 13),foreground=txt_color, background="white")
        self.mdp_entry.grid(row=1, column=1, pady=2, ipady=2)

    def bouton_connexion(self):

        style = ttk.Style()
        style.configure("Connexion.TButton", font=("Helvetica", 20), foreground="white", background="green")

        self.bp_connexion = ttk.Button(self.connexion_frame, text='Connexion', command=self.verifier_connexion, style="Connexion.TButton")
        self.bp_connexion.pack()

    def bouton_quitter(self):

        style = ttk.Style()
        style.configure("Quitter.TButton", font=("Helvetica", 13), foreground="white", background="red", width=8, height=6)

        self.bp_quitter = ttk.Button(self.quitter_frame, text="Quitter", command=self.click_quitter, style="Quitter.TButton")
        self.bp_quitter.grid(sticky="se")
        
####TODO tester la connexion######
    def click_connexion(self):   
        print("Button connexion")

    def click_quitter(self):

        MsgBox = messagebox.askquestion (
        title='Quitter Application',
        message='Etes vous sur de vouloir quitter ?',
        icon='warning')
        if MsgBox == 'yes':
            self.quit()

    def connect(self):
        
        ip_add = "http://172.31.11.13:8069"
        self.user_to_test = self.user_list.get()
        self.mdp_to_test = self.mdp_entry.get()

        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(ip_add))
            uid = common.authenticate('demo2', self.user_to_test, self.mdp_to_test, {})
            
            if uid:
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(ip_add))
                return models, xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(ip_add))
            else:
                print("Connexion échouée : Authentification impossible")
            return False
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            return False


    def verifier_connexion(self):
        print("Try to verif")
    
        self.connect()

        odoo_connection = self.connect()
        if odoo_connection:
            print("Connexion à Odoo réussie")
            self.ouvrir_page_utilisateur()
            # ne reste plus que à ouvrir la page asssocié à l'utilisateur        ouvrir_page_utilisateur(nom_utilisateur)
        else:
            print("Échec de connexion à Odoo")
            messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")
        
    def ouvrir_page_utilisateur(self):
        
        self.destroy()  # Fermer la fenêtre de connexion actuelle
        fenetre_utilisateur = None
        
        # Ouvrir une nouvelle page logistique
        if self.user_to_test == "Logistique":
            fenetre_utilisateur = visuLog() 
            fenetre_utilisateur.mainloop()
            
        # Ouvrir une nouvelle page production
            
        elif self.user_to_test == "Production":
            fenetre_utilisateur = visuprod() 
            fenetre_utilisateur.mainloop()
            

# Boucle principale
if __name__ == "__main__":
    myApp = App()
    myApp.mainloop()
