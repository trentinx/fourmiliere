from  ants import *
import sys


indexes = ["zero","un","deux","trois","quatre","cinq"]


i = 0
if len(sys.argv)==1:
    i = int(input("Merci d'entrer un entier compris entre 0 et 5 inclus : "))
else:
    i = int(sys.argv[1])

if i >= 0 and i < len(indexes): 
    filename = f"fourmiliere_{indexes[i]}.txt"
    print(f"Création de la fourmilière issue du fichier {filename}")
    anthill = Anthill(filename)
    print("\nDescription de la fourmiliere")
    anthill.print_nodes()
    draw_graph(anthill)
    draw_graph_step(anthill.nodes,"initiale")
    print("\nEtapes des déplacements des fourmis")
    anthill.move_all_ants()
    print(f"Taille de la population : {anthill.size}.")
    print(f"Nombres de fourmis arrivées dans le dortoir : {anthill.nodes['Sd'].nb_ants}.")
else:
    print("Le paramètre doit être compris entre 0 et 5 inclus")
