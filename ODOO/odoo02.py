import xmlrpc.client

# Informations de connexion Odoo
url = '10.0.2.15:8069'  # Remplacez par l'URL de votre instance Odoo
db = 'demo'
username = 'emilienqr@gmail.com'
password = '2000'

# Connexion
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid:
    # Si l'authentification réussit, ouvrez une nouvelle session
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    print("Connection OK")
    

else:
    print("Connexion échouée")
