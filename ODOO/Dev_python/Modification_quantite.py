import xmlrpc.client

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

def produit(models, db, uid, password):
    try:
        # Récupérer les données des articles depuis mrp.production
        articles = models.execute_kw(
            db, uid, password, 'mrp.production', 'search_read',
            [], {'fields': ['product_id', 'product_qty']}
        )

        # Afficher le nom et l'ID des articles
        for article in articles:
            article_id = article['product_id'][0] if article.get('product_id') else ''
            article_name = article['product_id'][1] if article.get('product_id') else ''
            print(f"Article ID: {article_id}, Nom: {article_name}")

    except Exception as e:
        print(f"Erreur lors de la récupération des articles : {e}")

# Utilisation de la fonction produit avec les paramètres
url = 'http://localhost:8069'
db = 'Pas_demo'
username = 'emilienqr@gmail.com'
password = '2000'

odoo_models, odoo_connection = connect(url, db, username, password)
if odoo_connection and odoo_models:
    print("Connexion réussie à Odoo")
    produit(odoo_models, db, 2, password)