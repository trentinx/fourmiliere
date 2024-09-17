import os

class Node:
    def __init__(self,name, max_ants=1,nb_ants=0):
        self.name = name
        self.next_nodes = []
        self.prec_nodes = []
        self.max_ants = max_ants
        self.nb_ants = nb_ants
        self.nb_ants_at_start = nb_ants
        self.lock = False

    def add_next(self, node):
        self.next_nodes.append(node)

    def add_pred(self,node):
        self.prec_nodes.append(node)



def create_anthill(filename):
    sd_append = True
    nb_ants = 0
    anthill = []
    with open(os.path.join("data","fourmilieres",filename),"r") as datafile:
        for line in datafile:
            line = line.strip("\n")
            if line.startswith("f="):
                nb_ants = int(line.split("=")[1])
                anthill.append(Node("Sv",nb_ants,nb_ants))
            elif "-" not in line:
                if "{" in line:
                    name,_,max_ants,_ = line.split()
                    anthill.append(Node(name,int(max_ants)))
                else:
                    anthill.append(Node(line))
            else:
                if sd_append:
                    anthill.append(Node("Sd",nb_ants,0))
                    sd_append = False
                src_nodename,_,tgt_nodename = line.split(" ")
                if src_nodename == "Sd" or tgt_nodename == "Sv":
                    tmp_nodename = src_nodename
                    src_nodename = tgt_nodename
                    tgt_nodename = tmp_nodename
                for node in anthill:
                    if node.name == src_nodename:
                        src_node = node
                    if node.name == tgt_nodename:
                        tgt_node = node
                        break
                src_node.add_next(tgt_node)
                tgt_node.add_pred(src_node)
    return anthill

def move_ants(current_node):
    if current_node.name != "Sv":
        for node in current_node.prec_nodes:
            if not node.lock and node.nb_ants > 0:  
                ants_to_move = min(current_node.max_ants - current_node.nb_ants , node.nb_ants)
                current_node.nb_ants += ants_to_move
                node.nb_ants -= ants_to_move
                current_node.lock = (current_node.nb_ants == current_node.max_ants)
                if ants_to_move > 0:
                    print(f"Move {ants_to_move} ants from {node.name} to {current_node.name}")
    for node in current_node.prec_nodes:
        move_ants(node)



# REmplacer le lock par le nombre de fourmis qui ont bougé et compter le nombres de fourmis présentes au début de l'étape dans chaque noeud