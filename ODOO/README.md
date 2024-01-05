# ODOO
Backup_data_base : Le dossier de sauvegarde des backups de la BDD
    -Backup du 03/01/2024

Dev_python : Dossier regroupant les fichiers de développement python des différentes fonctions
    - Création_article_admin : Code permettant de créer un article dans le stock.
    - Création_OF_VENTE : Code permettant de créer un OF de production d'un article => A débugguer : 
                                                                                                        - La saisie de l'ID de l'article ressort systématiquement un    article ARCHIVE. 
                                                                                                        - Impossible de supprimer l'OF après sa création depuis le code.
    - Lecture_article : Code permettant de lire la liste des artcile non archivés avec leurs images associés. => A revoir :
                                                                                                        - Le retour des images lors de l'éxecution du code.
    - Lecture_OF : Code permettant de lire la liste des OF non terminés et non annulés.
    - LOG_LOGISTIQUE : A supprimer.
    - main : Main du projetPython pour l'execution des fonctions.
    - TESTS_ODOO : Tous les codes liés au MAIN.

Documentation : Dossier regroupant les fichiers d'information.
    - Docker.compose-yml : Fichier pour la création du STACK Odoo15 dans portainer.
    - ERP : Fichier de tutoriel pour portainer.
    - MDP : Liste des mdp pour les logins 

