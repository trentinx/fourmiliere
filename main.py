from  ants import *

anthill = create_anthill("fourmiliere_trois.txt")

last_node = anthill[-1]
nb_ants = anthill[0].nb_ants



step = 1
while last_node.nb_ants != nb_ants:
    print(f"Step  {step} :")
    move_ants(last_node)
    print("----------------\n")
    step += 1
    for node in anthill:
        node.lock = False
