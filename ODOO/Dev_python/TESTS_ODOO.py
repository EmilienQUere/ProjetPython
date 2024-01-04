import xmlrpc.client
import base64

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

def Company(models, db, uid, password, company_name):

    try:
        company_id = models.execute_kw(db, uid, password,
                                       'res.company', 'search', 
                                       [[('name', '=', company_name)]], 
                                       {'limit': 1})
        if company_id:
            company_info = models.execute_kw(db, uid, password,
                                             'res.company', 'read', 
                                             [company_id[0]], 
                                             {'fields': ['phone', 'website']})
            return company_info[0] if company_info else None
        else:
            print(f"Entreprise '{company_name}' non trouvée.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'entreprise : {e}")
        return None
    
def Product(models, db, uid, password):
    
    try:
        product_ids = models.execute_kw(db, uid, password,
                                        'product.template', 'search_read', 
                                        [[]], 
                                        {'fields': ['id', 'name', 'list_price']})
        return product_ids if product_ids else None
    except Exception as e:
        print(f"Erreur lors de la recherche des produits : {e}")
        return None

def GetProductID(models, db, uid, password, product_name):

    try:
        product_id = models.execute_kw(db, uid, password,
                                       'product.product', 'search', 
                                       [[('name', '=', product_name)]], 
                                       {'limit': 1})
        if product_id:
            return product_id[0]
        else:
            print(f"Produit '{product_name}' non trouvé.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche du produit : {e}")
        return None

def SaveProductImage(models, db, uid, password, product_ID, image_name):


    try:
        product_fields = models.execute_kw(db, uid, password,
                                           'product.template', 'fields_get', 
                                           [], {'attributes': ['type']})
        image_field = next((field for field in product_fields if product_fields[field]['type'] == 'binary'), None)
        
        if image_field:
            product = models.execute_kw(db, uid, password,
                                        'product.template', 'read', 
                                        [product_ID], 
                                        {'fields': [image_field]})
            
            if product and product[0].get(image_field):
                image_data = base64.b64decode(product[0][image_field])
                with open(image_name + '.png', 'wb') as file:
                    file.write(image_data)
                print(f"L'image du produit avec l'ID {product_ID} a été sauvegardée sous {image_name}.png")
                return True
            else:
                print(f"Le produit avec l'ID {product_ID} n'a pas d'image.")
                return False
        else:
            print("Aucun champ d'image binaire trouvé pour product.template.")
            return False
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image du produit : {e}")
        return False
    
import base64


