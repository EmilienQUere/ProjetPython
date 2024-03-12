 Collaborateurs : Quere Emilien (manager)
                Esseul Antonin
                Le Roy Alexis

## Fichiers :

- Deskop_Tkinter : Dossier regroupant tous les développements sur python pour les utilisateurs LOGISTIQUE/PRODUCTION
- ODOO  : Dossier regroupant les back-ups de la base de données ODOO ainsi qu'un tutoriel de mise en service d'un serveur Odoo depuis Portainer.


# Pontage de la VM (WIFI Guest)

Afin que la machine physique et la VM soient sur le même réseau, il faut configurer un accès par pont dans l'onglet réseau dans la configuration de la VM

**L'opération est à réaliser sur les 3 VMs de l'application**

#### 1- Dans Oracle VM BOX sélectionnez la VM concernée. 
#### 2- Cliquez sur **Configuration**
#### 3- Sélectionnez l'onglet **Réseau**
#### 4- Dans le menu **Mode accès réseau** sélectionnez **Accès par pont**
#### 5- Démarrez la VM, elle sera sur le même réseau que la machine physique sur la WIFI Guest

Dans le lanceur d'application, onglet ordinateur, sélectionnez **Configuration du système**. Sélectionnez la rubrique Connexions (onglet Réseau). Dans l'onglet IPv4 passez de la Méthode Automatique à **Manuelle** puis cliquez sur Ajouter.
**Entrer l'adresse IPv4 de la VM1-PC1 qui héberge le serveur Odoo : entrez l'adresse IP suivante : 172.31.11.13**

# Installation de l'ERP ODOO sur la VM1 - PC1 Linux

#### 1- Préparation a l'installation :

Odoo à besoin d'un serveur Postgre SQL pour fonctionner correctement

Saisissez le code suivant dans l'invité de commande Linux
 ```
sudo apt install postgresql -y
 ```

Se connecter a internet (Mozilla Firefox) via : [erp](http://localhost:9000/#!/home) pour accéder au portainer

Un menu de connexion apparaît : 

Identifiant : **admin**

Mot de passe : **portainer**

Une fois les informations saisies, cliquez sur **Login**.

Vous allez être redirigés vers le menu principal de l'application, sélectionnez **l'endpoint local**.

Dans le menu affiché a gauche de l'écran, sélectionnez la rubrique **Stacks**.

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

Dans le menu **containers** cochez toutes les lignes de la colonne Name et cliquez sur **Start**.
Les serveurs sont démarrés.


#### 2- Restoration de la base de donnée :

Se connecter a l'adresse configurée dans le stack dans la barre de recherche du navigateur (`localhost:8069`) pour acceder a odoo

Cliquer sur **restore database**

Master password: 1308

Le fichier se trouve dans : ProjetPython/Odoo/Document/demo2_2024-03-11_12-31-54.zip **Il suffit d'aller le sélectionner dans l'explorateur de fichiers**

Database Name: demo2


# Une fois le Git importé dans le SSD et le serveur Odoo opérationnel : PC2-VM2 (Desktop Logistique sur Linux) et PC3-VM3 (Desktop Production sur Windows)
(Executer le code python)

#### 1- Ouvrir l'invite de commande

#### 2- Dans l'invite de commande :

Ouvrir le chemin du repository depuis l'invité de commande avec la fonction cd jusqu'a accéder au dossier Dev_Python
Exemple : 

```
cd /home/user/Documents/ProjetPython/Desktop_Tkinter/Dev_python
```
 
#### 3 - copier puis coller la commande dans l'invite de commande :  
Pour Linux :
``` 
python3 Page_Login.py
```
Pour Windows : 
``` 
python Page_Login.py
```
 
#### 4- Choisir le compte souhaité et entrez le mot de passe puis cliquer sur le bouton connexion


