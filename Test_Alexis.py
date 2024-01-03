# Test calculatrice simple

# Init variables
computer_price = 1000
wallet = int(input("combien d'argent avez vous ? "))

# Calcule achat
if computer_price < wallet:
    print ("l'achat est possible")
    wallet -= computer_price
    print ("Il vous reste " + str(wallet) + "$")

else : 
    print ("l'achat est impossible")
    print ("il vous manque {}$".format(computer_price - wallet))