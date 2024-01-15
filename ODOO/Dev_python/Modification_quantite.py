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

def update_stock(self):
        article_default_code = self.entry_ref.get()
        new_quantity = max(0, int(self.entry_quantity.get()))
 
        # Connexion à Odoo
        url = "http://localhost:8069"
        db = "demo"
        username = "emilienqr@gmail.com"
        password = "2000"
 
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
 
        # Recherche de l'ID de l'article par la référence interne
        article_id = models.execute_kw(db, uid, password, 'product.template', 'search', [[('default_code', '=', article_default_code)]])
        
        if article_id:
            # Rechercher les entrées du modèle stock.quant associées à l'article
            stock_entries = models.execute_kw(db, uid, password, 'stock.quant', 'search_read', [
                [('product_id', '=', article_id[0])]
            ])
 
            if stock_entries:
                # Mettre à jour la quantité en remplaçant par la nouvelle quantité
                new_stock_quantity = new_quantity
 
                # Mettre à jour la stock.quant associée à l'article
                models.execute_kw(db, uid, password, 'stock.quant', 'write', [stock_entries[0]['id'], {'quantity': new_stock_quantity}])
                print("Quantité en stock mise à jour avec succès.")
 
    
            else:
                print("Aucune entrée stock.quant trouvée pour l'article.")
        else:
            print("Article non trouvé.")
