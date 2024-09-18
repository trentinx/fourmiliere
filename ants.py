import os
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self,name, max_ants=1,nb_ants=0):
        self.name = name
        self.next_nodes = []
        self.prec_nodes = []
        self.max_ants = max_ants
        self.nb_ants = nb_ants
        self.ants_at_start = nb_ants

    def add_next(self, node):
        self.next_nodes.append(node)

    def add_pred(self,node):
        self.prec_nodes.append(node)


class Anthill:
    def __init__(self,filename):
        self.filename = filename
        sd_append = True
        size = 0
        nodes = {}
        with open(os.path.join("data","fourmilieres",filename),"r") as datafile:
            for line in datafile:
                line = line.strip("\n").strip(" ")
                if line.startswith("f="):
                    size = int(line.split("=")[1])
                    nodes["Sv"] = Node("Sv",size,size)
                elif "-" not in line:
                    if "{" in line:
                        name,_,max_ants,_ = line.split()
                        nodes[name] = Node(name,int(max_ants))
                    else:
                        nodes[line] = Node(line)
                else:
                    if sd_append:
                        nodes["Sd"] = Node("Sd",size,0)
                        sd_append = False
                    src_nodename,_,tgt_nodename = line.split(" ")
                    if src_nodename == "Sd" or tgt_nodename == "Sv":
                        tmp_nodename = src_nodename
                        src_nodename = tgt_nodename
                        tgt_nodename = tmp_nodename
                    nodes[src_nodename].add_next(nodes[tgt_nodename])
                    nodes[tgt_nodename].add_pred(nodes[src_nodename])
        self.nodes = nodes
        self.size = size
    
    def print_nodes(self, reverse=False):
        if not reverse:
            for node in self.nodes.values():
                for next_node in node.next_nodes:
                    print(f"{node.name} - {next_node.name}")
        else:
            for node in self.nodes.values().__reversed__():
                 for prec_node in node.prec_nodes:
                    print(f"{node.name} - {prec_node.name}")

    def move_all_ants(self):
        last_node = self.nodes["Sd"]
        nb_ants = self.size
        step = 1
        while last_node.nb_ants != nb_ants:
            print(f"Step  {step} :")
            move_ants(last_node)
            draw_graph_step(self.nodes,step)
            print("----------------\n")
            step += 1
            for node in self.nodes.values():
                node.ants_at_start = node.nb_ants


def move_ants(current_node):
    if current_node.name != "Sv":
        for node in current_node.prec_nodes:
            if node.ants_at_start > 0:
                ants_to_move = min(current_node.max_ants - current_node.nb_ants, node.ants_at_start)
                current_node.nb_ants += ants_to_move
                node.nb_ants -= ants_to_move
                node.ants_at_start -= ants_to_move
                if ants_to_move > 0:
                    print(f"Move {ants_to_move} ants from {node.name} to {current_node.name}")
    for node in current_node.prec_nodes:
        move_ants(node)



def draw_graph(anthill):
    G = nx.Graph()
    nodes = anthill.nodes
    nodes_list = list(nodes.keys())
    color_map = ["blue"]*len(nodes_list)
    color_map[0] = "red"
    color_map[-1] = "green"
    G.add_nodes_from(nodes_list)
    edges_list = []
    for node in nodes.values():
        for next_node in node.next_nodes:
            edges_list.append((node.name,next_node.name))
    G.add_edges_from(edges_list)
    plt.title(anthill.filename)
    nx.draw_planar(G, node_color=color_map, node_size=800, with_labels=True, font_weight='bold')
    plt.show()

def draw_graph_step(nodes,step):
    G = nx.Graph()
    values_list = [node.nb_ants for node in nodes.values()]
    nodes_list = list(nodes.keys()) 
    labels = {}
    for key,value in zip(nodes_list,values_list):
        labels[key] = value
    color_map = ["blue"]*len(nodes_list)
    for i,value in enumerate(values_list):
        if value > 0 :
            color_map[i] = "yellow"
    color_map[0] = "red"
    color_map[-1] = "green"
    G.add_nodes_from(nodes_list)
    edges_list = []
    for node in nodes.values():
        for next_node in node.next_nodes:
            edges_list.append((node.name,next_node.name))
    G.add_edges_from(edges_list)
    plt.title(f"Etape {step}")
    nx.draw_planar(G, node_color=color_map, node_size=800, labels=labels, with_labels=True, font_weight='bold')
    plt.show()
    