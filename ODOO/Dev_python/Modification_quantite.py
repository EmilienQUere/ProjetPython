import xmlrpc.client
from datetime import datetime

def connect(url, db, username, password):
    try:
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
            return models, uid
        else:
            print("Connexion échouée : Authentification impossible")
            return None, None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None, None

def modif_qty(order_id, new_quantity):
    try:
        # Connexion XML-RPC à Odoo
        url = "http://172.31.11.13:8069"
        db = "demo2"
        username = "your_username"
        password = "your_password"

        models, uid = connect(url, db, username, password)

        if models and uid:
            result = models.execute_kw(db, uid, 'your_password', 'product.product', 'write',
                [[order_id], {'qty_available': new_quantity}]
            )

            if result:
                print(f"Quantité dans le stock de l'article avec l'ID {order_id} modifiée avec succès.")
            else:
                print(f"La modification de la quantité dans le stock de l'article avec l'ID {order_id} a échoué.")
    except Exception as e:
        print(f"Erreur lors de la modification de la quantité dans le stock : {e}")


if __name__ == "__main__":
    # Connexion à Odoo
    url = "http://localhost:8069"
    db = "demo2"
    username = "administrateur"
    password = "2000"
    modif_qty(51, 24)
