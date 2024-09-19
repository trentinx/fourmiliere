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
    print("\nChemins possibles :")
    for path in anthill.get_paths():
        print(path)
    
    print(f"\nCycles :")
    for path in anthill.get_cycles():
        print(path)
   
else:
    print("Le paramètre doit être compris entre 0 et 6 inclus")

