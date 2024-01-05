import xmlrpc.client
from datetime import datetime

def connect(url, db, username, password):
    try:
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
            return models, xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        else:
            print("Connexion échouée : Authentification impossible")
            return None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

def AffOF(models, db, uid, password):
    try:
        # Récupérer les OF non terminés et non annulés
        of_records = models.execute_kw(
            db, uid, password, 'mrp.production', 'search_read',
            [[('state', 'not in', ['done', 'cancel'])]],
            {'fields': ['product_id', 'name', 'product_qty', 'date_planned_start', 'company_id', 'state']}
        )
        
        for of in of_records:
            article_name = of.get('product_id')[1] if of.get('product_id') else ''
            OF_ID = of.get('id')
            OF_Name = of.get('name')
            Quantity = of.get('product_qty')
            quantity_produced = of.get('quantity_produces', 0)
            date = datetime.strptime(of.get('date_planned_start'), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y %H:%M:%S')
            Society = of.get('company_id')[1] if of.get('company_id') else ''
            etat_OF = of.get('state')
            
            print(f"Article: {article_name}, OF ID: {OF_ID}, OF Name: {OF_Name}, Quantity: {Quantity}, "
                  f"Produced Quantity: {quantity_produced}, Date: {date}, Society: {Society}, Etat: {etat_OF}")
    except Exception as e:
        print(f"Erreur lors de la lecture des ordres de fabrication : {e}")

<<<<<<< HEAD
url = 'http://localhost:8069'
=======
# Exemple d'utilisation
url = 'http://172.31.11.13:8069'
>>>>>>> 79f3c4c0683d6fde2db6250dffe3e3fab4f95bf9
db = 'demo'
username = 'emilienqr@gmail.com'
password = '2000'

odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_connection and odoo_models:
    print("Connexion réussie à Odoo")
    AffOF(odoo_models, db, 2, password)