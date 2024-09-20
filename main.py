from  ants import *
import sys


indexes = ["zero","un","deux","trois","quatre","cinq","six"]


i = 0
if len(sys.argv)==1:
    i = int(input("Merci d'entrer un entier compris entre 0 et 6 inclus : "))
else:
    i = int(sys.argv[1])

if i >= 0 and i < len(indexes): 
    filename = f"fourmiliere_{indexes[i]}.txt"
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
    print("Le paramètre doit être compris entre 0 et 6 inclus")
