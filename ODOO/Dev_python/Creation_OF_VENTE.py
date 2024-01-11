import xmlrpc.client
from datetime import datetime

# Fonction de connexion à Odoo
def connect(url, db, username, password):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            return models, uid
        else:
            print("Connexion échouée : Authentification impossible")
            return None, None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None, None
    

    
# Fonction pour créer un ordre de fabrication
def create_manufacturing_order(models, uid, password, article_id, quantity, date, society):
    try:
        formatted_date = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
        
        manufacturing_order_id = models.execute_kw(
            db, uid, password, 'mrp.production', 'create',
            [{'product_id': article_id,
              'product_qty': quantity,
              'date_planned_start': formatted_date.strftime('%Y-%m-%d %H:%M:%S'),
              'company_id': society}]
        )
        
        print(f"Ordre de fabrication créé avec succès avec l'ID : {manufacturing_order_id}")
        return manufacturing_order_id
    except Exception as e:
        print(f"Erreur lors de la création de l'ordre de fabrication : {e}")
        return None

# Paramètres pour la création de l'ordre de fabrication
if __name__ == "__main__":
    url = 'http://localhost:8069'
    db = 'demo'
    username = 'emilienqr@gmail.com'
    password = '2000'
    article_id = 50  # Remplacez par l'ID de l'article à produire
    quantity = 10
    date = '08/02/2024 08:00:00'  # Remplacez par la date souhaitée au format 'JJ/MM/AAAA HH:MM:SS'
    society = 1  # Remplacez par l'ID de la société associée

    # Connexion à Odoo
    odoo_models, uid = connect(url, db, username, password)
    
    if odoo_models and uid:
        print("Connexion réussie à Odoo")
        create_manufacturing_order(odoo_models, uid, password, article_id, quantity, date, society)
    else:
        print("La connexion à Odoo a échoué.")

def get_product_uom_id(models, uid, password, product_id):
    try:
        product = models.execute_kw(
            db, uid, password,
            'product.product', 'read',
            [product_id],
            {'fields': ['product_uom_id']}
        )
        return product[0]['product_uom_id'][0] if product and product[0].get('product_uom_id') else None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'unité de mesure du produit : {e}")
        return None

# Appel de la fonction pour obtenir l'ID de l'unité de mesure
product_uom_id = get_product_uom_id(odoo_models, uid, password, article_id)
if product_uom_id:
    # Utilisation de l'ID de l'unité de mesure pour créer l'ordre de fabrication
    create_manufacturing_order(odoo_models, uid, password, article_id, quantity, date, society, product_uom_id)
else:
    print("Impossible de récupérer l'ID de l'unité de mesure du produit.")