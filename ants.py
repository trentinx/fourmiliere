import os
import networkx as nx
import matplotlib.pyplot as plt

class Room:
    def __init__(self,name, max_ants=1,nb_ants=0):
        self.name = name
        self.next_rooms = []
        self.prec_rooms = []
        self.max_ants = max_ants
        self.nb_ants = nb_ants
        self.ants_at_start = nb_ants

    def add_next(self, room):
        self.next_rooms.append(room)

    def add_pred(self,room):
        self.prec_rooms.append(room)


class Anthill:
    def __init__(self,filename):
        self.filename = filename
        sd_append = True
        size = 0
        rooms = {}
        with open(os.path.join("data","fourmilieres",filename),"r") as datafile:
            for line in datafile:
                line = line.strip("\n").strip(" ")
                if line.startswith("f="):
                    size = int(line.split("=")[1])
                    rooms["Sv"] = Room("Sv",size,size)
                elif "-" not in line:
                    if "{" in line:
                        name,_,max_ants,_ = line.split()
                        rooms[name] = Room(name,int(max_ants))
                    else:
                        rooms[line] = Room(line)
                else:
                    if sd_append:
                        rooms["Sd"] = Room("Sd",size,0)
                        sd_append = False
                    src_roomname,_,tgt_roomname = line.split(" ")
                    if src_roomname == "Sd" or tgt_roomname == "Sv":
                        tmp_roomname = src_roomname
                        src_roomname = tgt_roomname
                        tgt_roomname = tmp_roomname
                    rooms[src_roomname].add_next(rooms[tgt_roomname])
                    rooms[tgt_roomname].add_pred(rooms[src_roomname])
        self.rooms = rooms
        self.size = size
    
    def print_rooms(self, reverse=False):
        if not reverse:
            for room in self.rooms.values():
                for next_room in room.next_rooms:
                    print(f"{room.name} - {next_room.name}")
        else:
            for room in self.rooms.values().__reversed__():
                 for prec_room in room.prec_rooms:
                    print(f"{room.name} - {prec_room.name}")

    def move_all_ants(self):
        last_room = self.rooms["Sd"]
        nb_ants = self.size
        step = 1
        while last_room.nb_ants != nb_ants:
            print(f"Step  {step} :")
            move_ants(last_room)
            draw_graph(self,step)
            print("----------------\n")
            step += 1
            for room in self.rooms.values():
                room.ants_at_start = room.nb_ants
    
    def get_paths(self):
        current_path = None
        paths_list = [["Sv"]]
        paths_tmp = []
        for key,room in self.rooms.items():
            if key != "Sd":
                for path in paths_list:
                    if path[-1] == key:
                        for next_room in room.next_rooms:
                            current_path = path.copy()
                            current_path.append(next_room.name)
                            paths_tmp.append(current_path)
                    else:
                        current_path = path.copy()
                        paths_tmp.append(current_path)
                paths_list = paths_tmp.copy()
                paths_tmp = []
        return paths_list
    
    def get_cycles(self):
        cycles = []
        for path in self.get_paths():
            for node in path:
                if path.count(node) > 1:
                    cycles.append(path)
                    break
        return cycles

def move_ants(current_room):
    if current_room.name != "Sv":
        for room in current_room.prec_rooms:
            if room.ants_at_start > 0:
                ants_to_move = min(current_room.max_ants - current_room.nb_ants, room.ants_at_start)
                current_room.nb_ants += ants_to_move
                room.nb_ants -= ants_to_move
                room.ants_at_start -= ants_to_move
                if ants_to_move > 0:
                    print(f"Move {ants_to_move} ants from {room.name} to {current_room.name}")
    for room in current_room.prec_rooms:
        move_ants(room)
    

def draw_graph(anthill,step=None):
    G = nx.Graph()
    rooms = anthill.rooms
    rooms_list = list(rooms.keys()) 
    color_map = ["blue"]*len(rooms_list)
    labels = {}
    if  step:
        values_list = [room.nb_ants for room in rooms.values()]
        for key,value in zip(rooms_list,values_list):
            labels[key] = value
        for i,value in enumerate(values_list):
            if value > 0 :
                color_map[i] = "yellow"
    color_map[0] = "red"
    color_map[-1] = "green"
    G.add_nodes_from(rooms_list)
    edges_list = []
    for room in rooms.values():
        for next_room in room.next_rooms:
            edges_list.append((room.name,next_room.name))
    G.add_edges_from(edges_list)
    if step:
        title = f"Etape {step}"
    else:
        title = anthill.filename
    plt.title(title)
    if step:
        nx.draw_planar(G,node_color=color_map,
                   node_size=800, labels=labels, 
                   with_labels=True,font_weight='bold')
    else:
        nx.draw_planar(G,node_color=color_map,
                   node_size=800, with_labels=True,
                   font_weight='bold')
    pics_dir = get_pics_dir(anthill)
    #plt.savefig(os.path.join(pics_dir,str(step)))
    plt.show()
    
    
def get_pics_dir(anthill):
    pics_dirs = ["pics", 
                 os.path.join("pics",os.path.splitext(anthill.filename)[0])
                ]
    for dir in pics_dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)
    return pics_dirs[1]
    