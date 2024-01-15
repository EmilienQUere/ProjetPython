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
def create_manufacturing_order(models, uid, product_name, quantity, date, society, components_availability):
    try:
        # Recherche de l'ID du produit
        product_id = models.execute_kw(
            db, uid, password, 'product.product', 'search',
            [[('name', '=', product_name)]]
        )
        
        if not product_id:
            print(f"Erreur : Le produit '{product_name}' n'a pas été trouvé dans la base de données.")
            return None

        # Recherche de l'ID de la nomenclature associée au produit
        bom_id = models.execute_kw(
            db, uid, password, 'mrp.bom', 'search',
            [[('product_tmpl_id.product_variant_ids', 'in', [product_id[0]])]]
        )

        if not bom_id:
            print(f"La nomenclature pour le produit '{product_name}' n'a pas été trouvée. Création automatique de la nomenclature.")

            # Création automatique de la nomenclature
            bom_id = models.execute_kw(
                db, uid, password, 'mrp.bom', 'create',
                [{'product_tmpl_id': product_id[0]}]
            )
        else:
            print(f"Nomenclature trouvée pour le produit '{product_name}'.")

        # Recherche de l'ID de l'unité de mesure associée au produit
        product_uom_id = models.execute_kw(
            db, uid, password, 'product.product', 'read',
            [product_id[0]], {'fields': ['uom_id']}
        )[0]['uom_id'][0]

        # Conversion de la date
        formatted_date = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')

        # Création de l'ordre de fabrication sans 'component_status'
        manufacturing_order_id = models.execute_kw(
            db, uid, password, 'mrp.production', 'create',
            [{'product_id': product_id[0],
              'product_qty': quantity,
              'date_planned_start': formatted_date.strftime('%Y-%m-%d %H:%M:%S'),
              'company_id': society,
              'bom_id': bom_id[0],
              'product_uom_id': product_uom_id,
              'components_availability': components_availability}]
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
    username = 'administrateur'
    password = '2000'
    product_name = 'Joue de porc'  # Remplacez par le nom du produit à produire
    quantity = 10
    date = '08/02/2024 08:00:00'  # Remplacez par la date souhaitée au format 'JJ/MM/AAAA HH:MM:SS'
    society = 1  # Remplacez par l'ID de la société associée
    components_availability = 'Disponible'  # Ajout du champ 'component_availability'

    # Connexion à Odoo
    odoo_models, uid = connect(url, db, username, password)
    
    if odoo_models and uid:
        print("Connexion réussie à Odoo")
        create_manufacturing_order(odoo_models, uid, product_name, quantity, date, society, components_availability)
    else:
        print("La connexion à Odoo a échoué.")

