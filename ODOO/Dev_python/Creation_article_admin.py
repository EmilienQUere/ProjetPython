import xmlrpc.client
import base64

url = 'http://localhost:8069'
db = 'demo'
username = 'emilienqr@gmail.com'
password = '2000'
article_name = 'Tests'
sell_price = 100.0
product_price = 80.0
intern_reference = '155'
article_category = 3  # Remplacez par l'ID de la catégorie de l'article
article_type = 'product'  # Remplacez par le type d'article approprié ('product' ou 'service')
image_path = '/home/user/Bureau/ProjetPython/Joue de porc2.png'  # Remplacez par le chemin absolu de l'image
can_be_sell = True
can_be_buy = False

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


def CreateArticle(models, db, uid, password, article_name, sell_price, product_price,
                  intern_reference, article_category, article_type, image_path,
                  can_be_sell, can_be_buy):
    try:
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        article_id = models.execute_kw(db, uid, password, 'product.template', 'create', [{
            'name': article_name,
            'list_price': sell_price,
            'standard_price': product_price,
            'default_code': intern_reference,
            'categ_id': article_category,
            'type': article_type,
            'image_1920': encoded_image,
            'sale_ok': can_be_sell,
            'purchase_ok': can_be_buy,
        }])
        
        print(f"Article '{article_name}' créé avec succès avec l'ID : {article_id}")
        return article_id
    except Exception as e:
        print(f"Erreur lors de la création de l'article : {e}")
        return None

# Utilisation de la fonction CreateArticle() pour créer un nouvel article


odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_connection and odoo_models:
    print("Connexion réussie à Odoo")
    CreateArticle(odoo_connection, db, 2, password, article_name, sell_price, product_price,
                  intern_reference, article_category, article_type, image_path,
                  can_be_sell, can_be_buy)