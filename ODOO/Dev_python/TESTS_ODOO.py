import xmlrpc.client

<<<<<<< HEAD
# Utilisation de la fonction Company() pour récupérer l'identifiant d'une entreprise spécifique
=======

>>>>>>> dc584bd42b703a7987ba115fb8fdae7a27be0d59
url = 'http://172.31.11.13:8069'
db = 'demo'
username = 'emilienqr@gmail.com'
password = '2000'
company_name = 'Barbak'

<<<<<<< HEAD
def connect(url, db, username, password)  
=======

def connect(url, db, username, password):
   
>>>>>>> dc584bd42b703a7987ba115fb8fdae7a27be0d59
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/objects'.format(url))
            return models,xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        else:
            print("Connexion échouée : Authentification impossible")
            return None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_connection and odoo_models:
    print("Connexion réussie à Odoo")
 
    #model_name = 'res.partner'
    #partner_ids = odoo_connection.execute_kw(db, 2, password, model_name, 'search', [[]])
    #partners = odoo_connection.execute_kw(db, 2, password, model_name, 'read', [partner_ids])

    #for partner in partners:
        #print(partner)

def Company(models, db, uid, password, company_name):

    try:
        company_id = models.execute_kw(db, uid, password,
                                       'res.company', 'search', 
                                       [[('name', '=', company_name)]], 
                                       {'limit': 1})
        if company_id:
            return company_id[0]  # Renvoie le premier élément trouvé
        else:
            print(f"Entreprise '{company_name}' non trouvée.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'entreprise : {e}")
        return None

<<<<<<< HEAD
=======
# Utilisation de la fonction Company() pour récupérer l'identifiant d'une entreprise spécifique
>>>>>>> dc584bd42b703a7987ba115fb8fdae7a27be0d59
odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_models and odoo_connection:
    print("Connexion réussie à Odoo")
    company_id = Company(odoo_connection, db, 2, password, company_name)
    if company_id:
        print(f"L'identifiant de '{company_name}' est : {company_id}")