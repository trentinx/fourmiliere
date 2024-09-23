import sys
from  ants import Anthill

print(len(sys.argv))
if len(sys.argv) ==2 :
    filename = sys.argv[1]
    print(f"Création de la fourmilière issue du fichier {filename}")
    anthill = Anthill(filename)
    print("\nDescription de la fourmiliere")
    anthill.print_rooms()
    anthill.draw_graph()
    anthill.draw_graph("initiale")
    print("\nEtapes des déplacements des fourmis")
    anthill.move_all_ants()
    print(f"Taille de la population : {anthill.size}.")
    print(f"Nombres de fourmis arrivées dans le dortoir : {anthill.rooms['Sd'].nb_ants}.")
else:
    print("Usage:\npython main.py <filename> : filename est le nom du fichier qui \
            doit être dans data/fourmilieres")
