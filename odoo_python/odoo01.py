import xmlrpc.client

def Connect(ip='localhost', port=8069, password='2000'):
    # Informations de connexion à Odoo
    url = 'http://{}:{}/'.format(ip, port)
    db = 'demo'
    username = 'emilienqr@gmail.com'
    
    # Établir une connexion
    common = xmlrpc.client.ServerProxy('{}xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})

    # Vérifier si l'authentification a réussi
    if uid:
        print('Connection réussie.')
    else:
        print('Échec de la connexion.')

if __name__ == '__main__':
    # Utilisation par défaut avec localhost, port 8069 et mot de passe vide
    Connect()

    # Vous pouvez également spécifier une adresse IP différente et/ou un port
    # Connect(ip='192.168.1.100', port=8070)

    # Utilisation avec un mot de passe spécifié
    # Connect(password='votre_mot_de_passe')


