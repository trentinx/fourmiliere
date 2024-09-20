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
        with open(os.path.join("data","fourmilieres",filename),"r",encoding="utf-8") as datafile:
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
                        src_room_name, tgt_room_name = tgt_room_name, src_room_name
                    rooms[src_room_name].add_next(rooms[tgt_room_name])
                    rooms[tgt_room_name].add_pred(rooms[src_room_name])
        self.rooms = rooms
        self.distances = self.get_distances()
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
                if room.ants_at_start > 0 and \
                self.distances[current_room.name] < self.distances[room.name]:
                    ants_to_move = min(current_room.max_ants - current_room.nb_ants,
                                       room.ants_at_start)
                    current_room.nb_ants += ants_to_move
                    room.nb_ants -= ants_to_move
                    room.ants_at_start -= ants_to_move
                    if ants_to_move > 0:
                        print(f"Move {ants_to_move} ants from {room.name} to {current_room.name}")
        for room in current_room.prec_rooms:
            if self.distances[current_room.name] < self.distances[room.name]:
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
                room.ants_at_start = room.nb_ants

    def draw_graph(self,step=None):
        """
        Draw graph scheme.
            step (_type_, optional): If None, labels are rooms names otherwise
            labels are number of ants in each room. Defaults to None.
        """
        graph = nx.DiGraph()
        rooms = self.rooms
        rooms_list = list(rooms.keys())
        color_map = ["blue"]*len(rooms_list)
        labels = {}
        if  step:
            values_list = [room.nb_ants for room in rooms.values()]
            for key,value in zip(rooms_list,values_list):
                labels[key] = f"{value}"
            for i,value in enumerate(values_list):
                if value > 0 :
                    color_map[i] = "yellow"
        color_map[0] = "red"
        color_map[-1] = "green"
        graph.add_nodes_from(rooms_list)
        edges_list = []
        for room in rooms.values():
            for next_room in room.next_rooms:
                edges_list.append((room.name,next_room.name))
        graph.add_edges_from(edges_list)
        if step :
            title = f"Etape {step}"
        else:
            title = self.filename
        plt.title(title)
        if step:
            nx.draw_planar(graph,node_color=color_map,
                       node_size=800, labels=labels,
                       with_labels=True,font_weight='bold')
        else:
            nx.draw_planar(graph,node_color=color_map,
                       node_size=800, with_labels=True,
                       font_weight='bold')
        pics_dir = self.get_pics_dir()
        if not step:
            step = "graph"
        plt.savefig(os.path.join(pics_dir,str(step)))
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
        for directory in pics_dirs:
            if not os.path.exists(directory):
                os.mkdir(directory)
        return pics_dirs[1]


    def get_distances(self):
        """
        Compute distances between rooms and dormitory (the last room to reach)

        Returns:
            dict: keys are room names and values are the number of rooms to reach the dormitory.
        """
        prec_rooms = { key: [ prec_room.name for prec_room in room.prec_rooms ]
                    for key,room in self.rooms.items()}
        distances = { key : 0 for key in self.rooms}
        return self.explore("Sd",prec_rooms,distances,0)

    def explore(self,current_node,nodes_list,distances,distance):
        """
        Compute the distance between current_node and the dormitory.

        Args:
            current_node (str): A room name.
            nodes_list (dict): Key is a room name, value is the list of room names that
                precede the current_room.
            distances (dict): Keys are room names and values are the number of rooms
                to reach the dormitory.
            distance (int): The current distance.

        Returns:
            dict: keys are room names and values are the number of rooms
                to reach the dormitory.
        """
        if current_node != "Sv":
            distance += 1
            for node in nodes_list[current_node]:
                if distances[node] == 0  or distances[node] > distance:
                    distances[node] = distance
                    self.explore(node,nodes_list,distances,distance)
        return distances

__all__ = ["Anthill"]

if __name__ == "__main__":
    anthill = Anthill("fourmiliere_quatre.txt")
    print(anthill.distances)



