from  ants import *

anthill = Anthill("fourmiliere_cinq.txt")

last_node = anthill.nodes["Sd"]
nb_ants = anthill.size

step = 1
while last_node.nb_ants != nb_ants:
    print(f"Step  {step} :")
    move_ants(last_node)
    print("----------------\n")
    step += 1
    for node in anthill.nodes.values():
        node.ants_at_start = node.nb_ants
