# DESKOP Tkinter

Ce dossier regroupe les codes pythons des utilisateurs LOGISTIQUE ET PRODUCTION suivant le cahier des charges du client.


Page de login : -Logo de l'entreprise 
                -Nom d'utilisateur sous menu déroulant
                -Mot de passe à saisir manuellement.
                -Bouton de connexion a cliquer lorsque les zones de sasie (utilisateur/mot de passe) sont remplies.
                -Un bouton fermer pour annuler.

En fonction du login choisi : LOGISTIQUE OU PRODUCTION -> redirection vers la bonne page.
                
                -LOGISTIQUE : 
                                => Affichage des articles non archivés sous forme de tableau
                                => Lorsque l'on sélectionne un article : L'image de l'article s'affiche en dessous.
                                => Pour modifier la quantité dans le stock d'un article : Appui sur le bouton modifier + selection de la ligne du tableau correspondant à l'article souhaité, une pop-up s'affiche => Entrer la nouvelle valeur du stock.
                                => Un bouton déconnexion pour quitter l'application.
                
                -PRODUCTION : 
                                => Affichage des Odres de fabrication sous forme de tableau 
                                => Pour modifier la quantité produite d'un OF : Appui sur le bouton modifier + selection de la ligne du tableau correspondant à l'OF souhaité, une pop-up s'affiche => Entrer la nouvelle valeur de la quantité produite.
                                => Un bouton déconnexion pour quitter l'application.

Les logins ADMINISTRATEUR et VENTE : A la validation de l'identifiant et du mdp : ouvre le navigateur sur la page de LOGIN Odoo.