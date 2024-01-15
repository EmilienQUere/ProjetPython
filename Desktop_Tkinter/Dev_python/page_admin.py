from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Chemin vers le driver Chrome. Assurez-vous que le driver est téléchargé et le chemin correctement spécifié.
chrome_driver_path = '/chemin/vers/chromedriver'

# Créer une instance du navigateur Chrome
driver = webdriver.Firefox(executable_path=chrome_driver_path)

# Ouvrir la page de connexion
driver.get('URL_de_la_page_de_connexion')

# Remplir le formulaire de connexion
username_field = driver.find_element_by_name('nom_utilisateur')
password_field = driver.find_element_by_name('mot_de_passe')

username_field.send_keys('votre_nom_utilisateur')
password_field.send_keys('votre_mot_de_passe')

# Soumettre le formulaire en appuyant sur la touche "Entrée"
password_field.send_keys(Keys.RETURN)

# Attente pour s'assurer que la page a le temps de se charger (ajustez selon vos besoins)
time.sleep(5)

# Votre code ici - vous êtes maintenant connecté et pouvez interagir avec la page.

# Fermer le navigateur à la fin du script
driver.quit()
