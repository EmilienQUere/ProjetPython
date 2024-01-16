import json
from selenium import webdriver
import time

class ConnectionWeb():
    def __init__(self, config_path='Desktop_Tkinter/Dev_python/config.json', gecko_driver_path='Desktop_Tkinter/Dev_python/Driver/geckodriver'):
        self.config_path = config_path
        self.gecko_driver_path = gecko_driver_path
        self.url_odoo = 'http://172.31.11.13:8069'
        self.driver = None

    def load_config(self):
        try:
            with open(self.config_path) as config_file:
                config_data = config_file.read()

            if not config_data.strip():
                raise ValueError("Le fichier JSON est vide.")

            config = json.loads(config_data)

            nom_utilisateur = config.get("username")
            mot_de_passe = config.get("password")

            if not nom_utilisateur or not mot_de_passe:
                raise ValueError("Les clés 'username' et 'password' sont manquantes dans le fichier JSON.")

            return nom_utilisateur, mot_de_passe

        except FileNotFoundError:
            raise FileNotFoundError("Le fichier JSON n'a pas été trouvé.")
        except json.JSONDecodeError:
            raise ValueError("Erreur de décodage JSON. Assurez-vous que le fichier JSON est valide.")
        except Exception as e:
            raise Exception(f"Une erreur s'est produite : {str(e)}")

    def connect_to_odoo(self):
        try:
            nom_utilisateur, mot_de_passe = self.load_config()

            # Créez une instance du navigateur Firefox avec Selenium
            service = webdriver.FirefoxService(executable_path=self.gecko_driver_path)
            self.driver = webdriver.Firefox(service=service)

            # Accédez à la page de connexion Odoo
            self.driver.get(self.url_odoo)

            # Localisez les champs de connexion (adaptés à la structure HTML du site)
            champ_nom_utilisateur = self.driver.find_element("name", "login")
            champ_mot_de_passe = self.driver.find_element("name", "password")

            # Entrez les informations d'identification
            champ_nom_utilisateur.send_keys(nom_utilisateur)
            champ_mot_de_passe.send_keys(mot_de_passe)

            # Cliquez sur le bouton de connexion
            bouton_connexion = self.driver.find_element("xpath", "//button[contains(text(), 'Connexion')]")
            bouton_connexion.click()

            # Attendez quelques secondes pour que la page se charge (ajustez selon votre besoin)
            time.sleep(5)

            # Faites quelque chose après la connexion, par exemple, imprimez le titre de la page
            print(self.driver.title)

        except Exception as e:
            raise Exception(f"Une erreur s'est produite lors de la connexion : {str(e)}")
        
    def run(self):
        self.connect_to_odoo()

if __name__ == "__main__":
    connection_web = ConnectionWeb()
    connection_web.run()
