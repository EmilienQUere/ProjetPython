import xmlrpc.client

def Connect(ip='localhost', port=8069, password='2000'):
    # Informations de connexion à Odoo
    url = 'http://{}:{}/'.format(ip, port)
    db = 'demo'  # Utilisation de la base de données demo
    username = 'emilienqr@gmail.com'
    
    # Établir une connexion
    common = xmlrpc.client.ServerProxy('{}xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})

    # Vérifier si l'authentification a réussi
    if uid:
        print('Authentification réussie. UID: {}'.format(uid))
    else:
        print('Échec de l\'authentification.')
        return None

    # Afficher l'adresse URL de connexion
    print('Adresse URL de connexion à Odoo:', url)

    # Récupérer la version d'Odoo
    version = common.version()
    print('Version d\'Odoo:', version.get('server_version'))

    # Récupérer le modèle Odoo
    models = xmlrpc.client.ServerProxy('{}xmlrpc/2/object'.format(url))

    # Vérifier si la récupération du modèle est réussie
    if models:
        print('Connexion OK')
        return models
    else:
        print('Échec Connexion')
        return None

if __name__ == '__main__':
    # Utilisation par défaut avec localhost, port 8069 et mot de passe vide
    odoo_models = Connect()

    # Vous pouvez également spécifier une adresse IP différente et/ou un port
    # odoo_models = Connect(ip='192.168.1.100', port=8070)

    # Utilisation avec un mot de passe spécifié
    # odoo_models = Connect(password='votre_mot_de_passe')

    # Utiliser odoo_models pour effectuer des opérations avec le modèle Odoo
    if odoo_models:
        # Exemple: Lister les partenaires (clients) dans Odoo
        partner_ids = odoo_models.execute_kw('demo', uid, password, 'res.partner', 'search', [[]])
        partners = odoo_models.execute_kw('demo', uid, password, 'res.partner', 'read', [partner_ids], {'fields': ['name']})

        print('Liste des partenaires:')
        for partner in partners:
            print(partner['name'])
    else:
        print('Impossible d\'effectuer des opérations, modèle Odoo non disponible.')
