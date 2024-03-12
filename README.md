 Collaborateurs : Quere Emilien (manager)
                Esseul Antonin
                Le Roy Alexis

## Fichiers :

- Deskop_Tkinter : Dossier regroupant tous les développements sur python pour les utilisateurs LOGISTIQUE/PRODUCTION
- ODOO  : Dossier regroupant les back-ups de la base de données ODOO ainsi qu'un tutoriel de mise en service d'un serveur Odoo depuis Portainer.

# ERP ODOO

## 1- Préparation a l'installation :

[odoo](https://www.odoo.com/documentation/15.0/fr/administration/install/packages.html)

Odoo à besoin d'un serveur Postgre SQL pour fonctionner correctement

 ```sudo apt install postgresql -y```

Se connecter a internet via : [erp](http://localhost:9000/#!/home) pour accéder au portainer
Créer un stack : 
- nom : odoo15
- Saisir dans la zone :
   ```
  version: '2'
services:
  web:
    image: odoo:15.0
    depends_on:
      - mydb
    ports:
      - "8069:8069"
    environment:
    - HOST=mydb
    - USER=odoo
    - PASSWORD=myodoo
  mydb:
    image: postgres:13
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=myodoo
      - POSTGRES_USER=odoo
restart : Always
```
Lancer les containers dans l'onglet containers


## 2- Restoration de la base de donnée :

Se connecter a l'adresse configurée dans le stack (`localhost:8069`) pour acceder a odoo

Cliquer sur restore database

Master password: 1308
File: /home/user/Documents/ProjetPython/ODOO/Backup_data_base/demo2_2024-03-11_12-31-54.zip
Database Name: demo2


# Une fois le Git importé dans le SSD et le serveur Odoo opérationnel :
(Executer le code python)
 
## 1- ouvrir l'invite de commande

## 2- copier puis coller la commande dans l'invite de commande :

Ouvrir le chemin du repository depuis l'invité de commande avec la fonction cd jusqu'a accéder au dossier Dev_Python
Exemple : 

```cd /home/user/Documents/ProjetPython/Desktop_Tkinter/Dev_python```
 
## 3 - copier puis coller la commande dans l'invite de commande :  
 
``` python3 Page_Login.py ```

 
## 4- Choisir le compte souhaité et entrez le mot de passe puis cliquer sur le bouton connexion


