import xmlrpc.client

<<<<<<< HEAD
# Informations de connexion Odoo
url = '10.0.2.15:8069'  # Remplacez par l'URL de votre instance Odoo
=======
# Informations de connexion Odoo à distance
url = 'http://172.31.11.13:8069'  # Remplacez par l'adresse IP ou le nom de domaine de votre instance Odoo
>>>>>>> fa194d2df270954f0e7ef54f31e59287d4de1084
db = 'demo'
username = 'emilienqr@gmail.com'
password = '2000'

# Connexion à distance
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid:
    # Si l'authentification réussit, ouvrez une nouvelle session
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
     # Vérifier si la récupération du modèle est réussie
    if models:
        print('Connexion OK')

    print('Authentification réussie. UID: {}'.format(uid))
   # Afficher l'adresse URL de connexion
    print('Adresse URL de connexion à Odoo:', url)
 
    # Récupérer la version d'Odoo
    version = common.version()
    print('Version d\'Odoo:', version.get('server_version'))

else:
    print("Connexion échouée")
