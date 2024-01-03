import xmlrpc.client

def Connect(ip='localhost', port=8069):
    # Informations de connexion à Odoo
    url = 'http://{}:{}/'.format(ip, port)
    db = 'nom_de_votre_base_de_donnees'
    username = 'votre_nom_utilisateur'
    password = 'votre_mot_de_passe'

    # Établir une connexion
    common = xmlrpc.client.ServerProxy('{}xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})

    # Vérifier si l'authentification a réussi
    if uid:
        print('Authentification réussie. UID: {}'.format(uid))
    else:
        print('Échec de l\'authentification.')
        return

    # Afficher l'adresse URL de connexion
    print('Adresse URL de connexion à Odoo:', url)

    # Récupérer la version d'Odoo
    version = common.version()
    print('Version d\'Odoo:', version.get('server_version'))

if __name__ == '__main__':
    # Utilisation par défaut avec localhost et port 8069
    Connect()

