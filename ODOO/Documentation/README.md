# ERP ODOO

## 1- Préparation a l'installation :

[odod](https://www.odoo.com/documentation/15.0/fr/administration/install/packages.html)

Odoo à besoin d'un serveur Postgre SQL pour fonctionner correctement

 `sudo apt install postgresql -y`

Se connecter a internet via : [erp](http://localhost:9000/#!/home) pour accéder au portainer
Créer un stack : odoo15 (cf. **docker-compose.yml**)
Lancer les containers


## 2- Restoration de la base de donnée :

Se connecter a l'adresse configurée dans le stack (`localhost:8069`) pour acceder a odoo

Cliquer sur restore database

Master password: 1308
File: /home/user/Documents/ProjetPython/ODOO/Backup_data_base/demo2_2024-03-11_12-31-54.zip
Database Name: demo2

