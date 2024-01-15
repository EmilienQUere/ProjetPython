import xmlrpc.client
from datetime import datetime
from PIL import Image
import io
import base64

#==========================================================================================================================================#

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

def AffichageArticles(models, db, uid, password):
    try:
        # Récupérer tous les articles
        article_records = models.execute_kw(
            db, uid, password, 'product.product', 'search_read',
            [[]],
            {'fields': ['name', 'default_code', 'list_price', 'standard_price', 'categ_id', 'image_1920']}
        )

        for article in article_records:
            article_nom = article.get('name')
            #article_ID = article.get('id')
            Prix_vente = article.get('list_price')
            Cout = article.get('standard_price')
            article_code = article.get('default_code')
            categorie_article = article.get('categ_id')[1] if article.get('categ_id') else ''

            # Récupérer les données de l'image de l'article
            image_data = article.get('image_1920')
            if image_data:
                # Convertir les données binaires de l'image en format image
                image_stream = io.BytesIO(base64.b64decode(image_data))
                img = Image.open(image_stream)
                
                # Afficher les détails de l'article avec l'image
                print(f"Nom: {article_nom}, ID: {article_code}, Prix de vente: {Prix_vente}, "
                      f"Coût: {Cout}, Catégorie: {categorie_article}")
                
                # Afficher l'image
                #img.show()
            else:
                # Afficher les détails de l'article sans image
                print(f"Nom: {article_nom}, ID: {article_code}, Prix de vente: {Prix_vente}, "
                      f"Coût: {Cout}, Catégorie: {categorie_article} - Aucune image")

    except Exception as e:
        print(f"Erreur lors de la récupération et de l'affichage des articles : {e}")

#==========================================================================================================================================#

# Utilisation de la fonction AffichageArticles avec le champ 'image_1920'
if __name__=="__main__":
    url = 'http://172.31.11.13:8069'
    db = 'demo'
    username = 'administrateur'
    password = '2000'

    odoo_models, odoo_connection = connect(url, db, username, password)
    if odoo_connection and odoo_models:
        print("Connexion réussie à Odoo")
        AffichageArticles(odoo_models, db, 2, password)