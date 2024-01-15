import TESTS_ODOO

#Déclaration des variables générales
url = 'http://172.31.11.13:8069' # Nom de l'hébergeur Odoo
db = 'demo' # Nom de la base de données
username = 'administrateur' # Nom d'utilisateur du login
password = '2000' # Mot de passe du login 
company_name = 'Barbak' # Nom de l'entreprise pour visualisation des détails
product_name = 'Lardons' # Nom du produit pour visualisation des détails
product_ID = 45  # identifiant du produit souhaité pour enregistrer son image
image_name = 'Joue de porc2' #Choix du nom d'enregistrement de l'image  

#Connexion a Odoo via les informations en tête du fichier main
odoo_models, odoo_connection = TESTS_ODOO.connect(url, db, username, password)
if odoo_connection and odoo_models:
        print("Connexion réussie à Odoo")

        #Récupération des informations sur l'entreprise (Nom,site web, ID)
        company_id = TESTS_ODOO.Company(odoo_connection, db, 2, password, company_name)
        if company_id:
            print(f"Les informations de l'entreprise '{company_name}' sont les suivantes : {company_id}")

        #Récupération des de tous les produits de la BDD (ID, Nom, Prix)
        products = TESTS_ODOO.Product(odoo_connection, db, 2 , password)
        if products:
            for product in products:
                print(f"ID: {product.get('id')}, Nom: {product.get('name')}, Prix: {product.get('list_price')}€")

       #Récupération des informations d'un produit au choix (Product_name)
        product_id = TESTS_ODOO.GetProductID(odoo_connection, db, 2, password, product_name)
        if product_id:
            print(f"L'identifiant de '{product_name}' est : {product_id}")

        #Sauvegarde de l'image du produit de la DB seléctionnée
        TESTS_ODOO.SaveProductImage(odoo_connection, db, 2, password, product_ID, image_name)
        