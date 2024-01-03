# programme calcule de hauteur

nb_boite = int(input("Entrez le nombre de boite :"))
if nb_boite < 1:
    nb_boite = 1
elif nb_boite > 100:
    nb_boite = 100
print (nb_boite)
nb_couche = int(input("Entrez le nombre de boite par couche (4,5,6 ou 9):"))
h_couche = nb_boite/nb_couche
h = h_couche*0.25
print("la hauteur est de {}m".format(h))