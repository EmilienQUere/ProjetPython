import os
import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label
from PIL import ImageTk, Image
import threading
import time
import xmlrpc.client
import socket
import subprocess
from Page_Logistique import AppLog as visuLog
from Page_Production import AppProd as visuProd

bg_color = "#f1f1f1"
txt_color = "#34494A"
image_path = os.path.abspath("BARBAK.png")

class App(tk.Tk):
    """ Application GUI in TKinter"""

    def __init__(self):
        """ Application constructor (heritage=Tk object)"""
        super().__init__()
        self.mdp_to_test = ''
        self.connexion_status = None
        
        self.screen_h = 500
        self.screen_v = 650
        self.screen_x = int((self.winfo_screenwidth()/2) - (self.screen_h/2))
        self.screen_y = 0
        geometry = str(self.screen_h)+"x"+str(self.screen_v)+"+"+str(self.screen_x)+"+"+str(self.screen_y)
        self.geometry(geometry)
        self.resizable(True, True)
        self.minsize(380, 600)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.attributes('-alpha', 1)
        self.config(bg=bg_color)
        self.iconphoto(False, tk.PhotoImage(file=image_path))
        self.title("Login Barbak")

        """Appel des fonctions"""
        self.frame()
        self.widget_texte()
        self.widget_image()
        self.user()
        self.mot_de_passe()
        self.bouton_connexion("green")
        self.bouton_quitter()
        self.save_mdp_to_test()
        self.check_connection()


    def frame(self):
        self.middle_frame = Frame(self, width=250, height=500, bg=bg_color)
        self.middle_frame.pack(side="top")

        self.log_frame = Frame(self.middle_frame, width=250, height=600, bg=bg_color)
        self.log_frame.pack(side="bottom", pady=20)

        self.connexion_frame = Frame(self, width=250, height=500, bg=bg_color)
        self.connexion_frame.pack()

        self.quitter_frame = Frame(self, width=100, height=125, bg=bg_color)
        self.quitter_frame.pack(side="bottom", anchor="e")

        # Ajouter une étiquette pour afficher le statut de la connexion
        self.connexion_status = Label(self.middle_frame, text="", font=("Helvetica", 13), foreground=txt_color, background=bg_color)
        self.connexion_status.pack(pady=10)

    def widget_texte(self):
        self.message = ttk.Label(self.middle_frame, text="Login", font=("Helvetica", 50), foreground=txt_color, background=bg_color)
        self.message.pack(ipady=20)

    def widget_image(self):
        mon_image = Image.open(image_path)
        resized_image = mon_image.resize((225, 225), Image.LANCZOS)
        self.new_image = ImageTk.PhotoImage(resized_image)
        self.image = ttk.Label(self.middle_frame, image=self.new_image)
        self.image.pack()

    def user(self):
        utilisateurs = {"Production", "Logistique"}
        self.user = ttk.Label(self.log_frame, text="Nom d'utilisateur", font=("Helvetica", 13), foreground=txt_color, background=bg_color)
        self.user.grid(row=0, column=0, pady=10, ipadx=5, ipady=5)
        self.user_list = ttk.Combobox(self.log_frame, values=list(utilisateurs), font=("Helvetica", 13), foreground="black", background="white")
        self.user_list.grid(row=0, column=1, pady=2, ipady=2)
        self.user_list.set(list(utilisateurs)[0])

    def mot_de_passe(self):
        self.mdp = ttk.Label(self.log_frame, text="Mot de passe", font=("Helvetica", 13), foreground=txt_color, background=bg_color)
        self.mdp.grid(row=1, column=0, pady=10, ipadx=5, ipady=5)
        self.mdp_entry = ttk.Entry(self.log_frame, show="*", font=("Helvetica", 13), foreground=txt_color, background="white")
        self.mdp_entry.grid(row=1, column=1, pady=2, ipady=2)

    def bouton_connexion(self, color):
        style = ttk.Style()
        style.configure("Connexion.TButton", font=("Helvetica", 20), foreground="white", background=color)
        self.bp_connexion = ttk.Button(self.connexion_frame, text='Connexion', command=self.verifier_user, style="Connexion.TButton")
        self.bp_connexion.pack()

    def bouton_quitter(self):
        style = ttk.Style()
        style.configure("Quitter.TButton", font=("Helvetica", 13), foreground="white", background="red", width=8, height=6)
        self.bp_quitter = ttk.Button(self.quitter_frame, text="Quitter", command=self.click_quitter, style="Quitter.TButton")
        self.bp_quitter.grid(sticky="se")

    def click_quitter(self):
        MsgBox = messagebox.askquestion (
        title='Quitter Application',
        message='Etes vous sur de vouloir quitter ?',
        icon='warning')
        if MsgBox == 'yes':
            self.stop_ping_thread()
            self.quit()
            
    def connect(self):
        ip_add = "http://172.31.11.13:8069"
        self.user_to_test = self.user_list.get()
        self.mdp_to_test = self.mdp_entry.get()

        try:
            socket.setdefaulttimeout(5)
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(ip_add))
            uid = common.authenticate('demo2', self.user_to_test, self.mdp_to_test, {})

            if uid:
                self.connexion_status.config(text="Connexion établie", foreground="green")
                return True
            else:
                print("Connexion échouée : Authentification impossible")
                self.mdp_to_test = ''
                messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")
                return False
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            self.connexion_status.config(text="Échec de connexion", foreground="red")
            return False

    def verifier_user(self):
        print(self.test_connection_odoo())
        if self.test_connection_odoo():

            print("Vérification de la connexion")
            if self.connect():
                print("Connexion à Odoo réussie")
                self.save_mdp_to_test()
                self.ouvrir_page_utilisateur()

    def save_mdp_to_test(self):
        with open("test.txt", "w") as file:
            file.write(self.mdp_to_test)

    def ouvrir_page_utilisateur(self):
        self.destroy()
        fenetre_utilisateur = None
        print(f"Connexion à la page {self.user_to_test}")

        if self.user_to_test == "Logistique":
            fenetre_utilisateur = visuLog()
            fenetre_utilisateur.mainloop()
        elif self.user_to_test == "Production":
            fenetre_utilisateur = visuProd()
            fenetre_utilisateur.mainloop() 

    def myping(self):
        try:
            # Exécutez la commande ping avec un seul paquet et un timeout de 1 seconde
            letter = "-n"  # Sur Windows, utilisez "-n"
            if os.name == 'posix':
                letter = "-c"  # Sur POSIX (Linux, macOS), utilisez "-c"
                    
            # Exécutez la commande ping avec un seul paquet et un timeout de 1 seconde
            subprocess.run(["ping", letter, "1", "172.31.11.13"], timeout=1, check=True)
            return True  # Si la commande ping réussit, retournez True
            
        except subprocess.TimeoutExpired:
            # Si le délai d'attente est expiré, considérez le ping comme un échec et retournez False
            return False
        except subprocess.CalledProcessError:
            # Si la commande ping échoue pour une autre raison, considérez le ping comme un échec et retournez False
            return False

    def check_connection(self):
        threading.Thread(target=self.check_ping).start()

    def check_ping(self):
        self.ping_thread_flag = True

        while self.ping_thread_flag:
            if self.myping():
                self.connexion_status.config(text="Connexion établie", foreground="green")
                self.test_connection_odoo()
            else:
                print("Ping échoué")
                self.connexion_status.config(text="Échec de la connexion à la machine", foreground="red")

            # Attendez 5 secondes avant la prochaine vérification
            time.sleep(5)

    def stop_ping_thread(self):
        self.ping_thread_flag = False

    def test_connection_odoo(self):
    
        try:
            # Connexion au serveur Odoo en utilisant XML-RPC
            common = xmlrpc.client.ServerProxy(f"http://172.31.11.13:8069/xmlrpc/2/common")
            # Récupération de la version d'Odoo
            version = common.version()
            if version != "":
                # Affichage de l'adresse URL de connexion et de la version d'Odoo
                print(f"Connexion réussie à Odoo sur : http://172.31.11.13:8069")
                print(f"Version de Odoo : {version['server_version']}")
                return True
            else:
                return False
            
        except Exception as e:
            print(f"Erreur lors de la connexion à Odoo : {e}")
            self.connexion_status.config(text="Échec de la connexion au serveur Odoo", foreground="red")
            return False
        
# Boucle principale
if __name__ == "__main__":
    myApp = App()
    myApp.mainloop()

