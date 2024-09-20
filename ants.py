
import os
import networkx as nx
import matplotlib.pyplot as plt

class Room:
    def __init__(self,name, max_ants=1,nb_ants=0):
        """
        Room constructor

        Args:
            name (str): Room name
            max_ants (int, optional): Max number of ants that can be simultaneously
                in the room. Defaults to 1.
            nb_ants (int, optional): Number of ants in the room. Defaults to 0.
        """
        self.name = name
        self.next_rooms = []
        self.prec_rooms = []
        self.max_ants = max_ants
        self.nb_ants = nb_ants
        self.ants_at_start = nb_ants

    def add_next(self, room):
        """
        Add a room to the list of neighbours that come right after.

        Args:
            room (Room): A Room object.
        """
        self.next_rooms.append(room)

    def add_pred(self,room):
        """
        Add a room to the list of neighbours that come right before.

        Args:
            room (Room): A Room object.
        """
        self.prec_rooms.append(room)


class Anthill:
    def __init__(self,filename):
        """
        Anthill Constructor, a dictionnary of Room objects.
        Args:
            filename (str): The name of the file that describe the anthill.
                The file must be in data/fourmilieres directory.
        """
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
                    src_room_name,_,tgt_room_name = line.split(" ")
                    if src_room_name == "Sd" or tgt_room_name == "Sv":
                        tmp_room_name = src_room_name
                        src_room_name = tgt_room_name
                        tgt_room_name = tmp_room_name
                    rooms[src_room_name].add_next(rooms[tgt_room_name])
                    rooms[tgt_room_name].add_pred(rooms[src_room_name])
        self.rooms = rooms
        self.size = size
        self.filename = filename

        
    
    def print_rooms(self, reverse=False):
        """
        Print line by line by pair rooms and their neighbours.

        Args:
            reverse (bool, optional): If False, pairs returned are room and next room,
                otherwise, room and precedent room. Defaults to False.
        """
        if not reverse:
            for room in self.rooms.values():
                for next_room in room.next_rooms:
                    print(f"{room.name} - {next_room.name}")
        else:
            for room in self.rooms.values().__reversed__():
                 for prec_room in room.prec_rooms:
                    print(f"{room.name} - {prec_room.name}")

    def move_ants(self,current_room):
        """
        Move ants from precedent rooms to the current room.

        Args:
            current_room (Room): The room where ants are moving.
        """
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
            self.move_ants(room)
    
    def move_all_ants(self):
        """
        Move all ants from vestibule to dormitory.
        """
        last_room = self.rooms["Sd"]
        nb_ants = self.size
        step = 1
        while last_room.nb_ants != nb_ants:
            print(f"Step  {step} :")
            self.move_ants(last_room)
            self.draw_graph(step)
            print("----------------\n")
            step += 1
            for room in self.rooms.values():
                room.ants_at_start = room.nb_ant

    def draw_graph(self,step=None):
        """
        Draw graph scheme.
            step (_type_, optional): If None, labels are rooms names otherwise
            labels are number of ants in each room. Defaults to None.
        """
        G = nx.Graph()
        rooms = self.rooms
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
            title = self.filename
        plt.title(title)
        if step:
            nx.draw_planar(G,node_color=color_map,
                       node_size=800, labels=labels, 
                       with_labels=True,font_weight='bold')
        else:
            nx.draw_planar(G,node_color=color_map,
                       node_size=800, with_labels=True,
                       font_weight='bold')
        pics_dir = self.get_pics_dir()
        #plt.savefig(os.path.join(pics_dir,str(step)))
        plt.show()
    
    
    def get_pics_dir(self):
        """
        Get the directory where we aim to save pictures generated by draw_graph method.

        Returns:
            str: A directory path.
        """
        pics_dirs = ["pics", 
                     os.path.join("pics",os.path.splitext(self.filename)[0])
                    ]
        for dir in pics_dirs:
            if not os.path.exists(dir):
                os.mkdir(dir)
        return pics_dirs[1]


def build_paths(graph,node,paths):
    if node == "Sd":
        return paths
    paths_list = paths.copy()
    tmp_paths_list = []
    next_nodes = graph[node]
    for next_node in next_nodes:
        #print(f"Next node is {next_node}")
        for path in paths_list:
            #print(f"Current path is {path}")
            if path[-1] == node:
                #print(f"{path} ends by {node}")
                tmp_path = path.copy()
                tmp_path.append(next_node)
                if tmp_path not in tmp_paths_list:
                    tmp_paths_list.append(tmp_path.copy())
            else:
                #print(f"{path} doesn't end by {node}")
                if path not in tmp_paths_list:
                    tmp_paths_list.append(path)
    paths_list = tmp_paths_list.copy()
    for next_node in next_nodes:
        paths_list=build_paths(graph,next_node,paths_list)
    return paths_list

            

    
if __name__ == "__main__":
    anthill = Anthill("fourmiliere_cinq.txt")