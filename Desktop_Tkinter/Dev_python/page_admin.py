from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Chemin vers le driver Chrome. Assurez-vous que le driver est téléchargé et le chemin correctement spécifié.
Firefox_driver_path = '/usr/local/bin/geckodriver'

# Créer une instance du navigateur Chrome
driver = webdriver.Firefox(Firefox_driver_path)

# Ouvrir la page de connexion
driver.get('http://172.31.11.13:8069/web/login')

# Attente pour s'assurer que la page a le temps de se charger (ajustez selon vos besoins)
time.sleep(5)

# Remplir le formulaire de connexion
username_field = driver.find_element_by_name('login')
password_field = driver.find_element_by_name('password')

username_field.send_keys('administrateur')
password_field.send_keys('2000')

# Soumettre le formulaire en appuyant sur la touche "Entrée"
password_field.send_keys(Keys.RETURN)

