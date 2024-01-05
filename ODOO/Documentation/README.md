# ERP ODOO

## 1- Préparation a l'installation :

[odod](https://www.odoo.com/documentation/15.0/fr/administration/install/packages.html)

Odoo à besoin d'un serveur Postgre SQL pour fonctionner correctement

 `sudo apt install postgresql -y`

Se connecter a internet via : [erp](http://localhost:9000/#!/home) pour accéder au portainer
Créer un stack : odoo15 (cf. **docker-compose.yml**)

Se connecter a l'adresse configurée dans le stack (`localhost:8069`) pour acceder a odoo
