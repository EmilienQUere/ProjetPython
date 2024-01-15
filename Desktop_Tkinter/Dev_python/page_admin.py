from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Remplacez ces valeurs par les informations de connexion appropriées
username = "administrateur"
password = "2000"
url = "https://example.com"  # Remplacez par l'URL du site web

# Utilisation de Selenium pour automatiser le navigateur Firefox
driver = webdriver.Firefox()  # Assurez-vous que geckodriver est dans le PATH
driver.get(url)

# Attendre que la page se charge (ajuster le temps d'attente si nécessaire)
time.sleep(2)

# Trouver les champs de saisie du nom d'utilisateur et du mot de passe
username_field = driver.find_element_by_name("username")  # Remplacez par le nom réel de l'élément HTML
password_field = driver.find_element_by_name("password")  # Remplacez par le nom réel de l'élément HTML

# Saisir les informations de connexion
username_field.send_keys(username)
password_field.send_keys(password)

# Soumettre le formulaire
password_field.send_keys(Keys.RETURN)

# Attendre que la connexion soit effectuée (ajuster le temps d'attente si nécessaire)
time.sleep(5)

