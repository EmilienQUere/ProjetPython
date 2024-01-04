import xmlrpc.client
import datetime

url = 'http://localhost:8069'
db = 'demo'
username = 'emilienqr@gmail.com'
password = '2000'
article_id = 43  # Remplacez par l'ID de l'article à produire
quantity = 10
date = '08/02/24 08:00:00'  # Remplacez par la date souhaitée au format 'JJ/MM/AA HH:MM:SS'
society = 1  # Remplacez par l'ID de la société associée

def connect(url, db, username, password):
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
    
    #Connexion a Odoo via les informations en tête du fichier main
odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_connection and odoo_models:
        print("Connexion réussie à Odoo")

def CreateOF(models, db, uid, password, article_id, quantity, date, society):
   
    try:
        formatted_date = datetime.strptime(date, '%d/%m/%y %H:%M:%S')
        
        of_id = models.execute_kw(db, uid, password, 'mrp.production', 'create', [{
            'product_id': article_id,
            'product_qty': quantity,
            'date_planned_start': formatted_date.strftime('%Y-%m-%d %H:%M:%S'),
            'company_id': society,
        }])
        
        print(f"Ordre de fabrication créé avec succès avec l'ID : {of_id}")
        return of_id
    except Exception as e:
        print(f"Erreur lors de la création de l'ordre de fabrication : {e}")
        return None

# Utilisation de la fonction CreateOF() pour créer un nouvel ordre de fabrication

odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_connection and odoo_models:
    print("Connexion réussie à Odoo")
    uid = odoo_models.execute_kw(db, 1, password, 'res.users', 'search', [[('login', '=', username)]])
    if uid:
        uid = uid[0]
        CreateOF(odoo_models, db, uid, password, article_id, quantity, date, society)
    else:
        print("Impossible de récupérer l'uid de l'utilisateur.")