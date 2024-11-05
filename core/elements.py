import json
import matplotlib.pyplot as plt
import numpy as np
from blinker import signal
from networkx.algorithms.bipartite.basic import color
from core.parameters import c

#classe che definisce le caratteristiche del segnale che deve essere propagato
class Signal_information(object):
    def __init__(self,signal_power, path): #constructor
        self._signal_power = signal_power
        self._latency = 0
        self._noise_power = 0
        self._path = path

    @property
    def signal_power(self): #property
        return self._signal_power

    def update_signal_power(self,added_value):
        self._signal_power = self._signal_power + added_value

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self,set_value):
        self._noise_power = set_value

    def update_noise_power(self, added_value):
        self._noise_power += added_value

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, set_value):
        self._latency = set_value

    def update_latency(self,added_value):
        self._latency += added_value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, set_value):
        self._path = set_value

    def update_path(self):
        if len(self.path) > 0:
            self._path = self._path[1:] #una volta attraversato il nodo vine rimosso dal path rimanente
            # per esempio se ho "ABC" e passo 'A', il nuovo path è "BC"

#Classe per istanziare tutti i nodi presente nel network. Le singole istanze vengono dichiarate in Network-> definito da un dizionario letto dal file json in Network
class Node(object):
    def __init__(self,label,position, connected_nodes):
        self._label = label
        self._position = position
        self._connected_nodes = connected_nodes
        self._successive = {} #dizionario di tutte le linee successive all'istnaza del NODO
        #esempio: nell'istnaza del nodo 'A' avrò successive: {AB:B, AC:C..} dove B e C sono i nodi successivi alla linea

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self,successive_dict):
        self._successive = successive_dict

    def propagate(self,signal_information):
        if len(signal_information.path) < 2:
            return
        next_line = signal_information.path[:2]
        signal_information.update_path()
        if next_line in self._successive:
            self.successive[next_line].propagate(signal_information)


#Classe per istanziare tutte le linee presenti nel network. Le singole istanze vengono dichiarate in Network-> definito da un dizionario letto dal file json in Network
class Line(object):
    def __init__(self,label,length):
        self._label = label
        self._length = length
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, set_value):
        self._successive = set_value

    def latency_generation(self):
        return self._length/(2/3*c)

    def noise_generation(self, signal_power):
        return signal_power * 1e-9 * self._length

    def propagate(self,signal_information):
        signal_information.update_latency(self.latency_generation())
        signal_information.update_noise_power(self.noise_generation(signal_information.signal_power))

        next_node = signal_information.path[0]

        if next_node in self._successive:
            self.successive[next_node].propagate(signal_information)
       

class Network(object):
    def __init__(self,file_in):
        self._nodes = {}
        self._lines = {}

        with open( file_in ,'r') as file:
            data = json.load(file)
        #creo la lista di nodi a partire dal file json
        for element in data:
            self._nodes[element] = Node(label=element,position=data[element]["position"],connected_nodes=data[element]["connected_nodes"])
        #creo la lista di linee aggiungendo la lunghezza
        for element in self._nodes:
            for connected_node in self._nodes[element].connected_nodes:
                #distanza euclidea con numpy
                punto_a = np.array(self._nodes[connected_node].position)
                punto_b = np.array(self._nodes[element].position)
                math_length = np.linalg.norm(punto_a - punto_b)
                #le linee vengono create in entrambi i sensi
                self._lines[element+connected_node] = Line(label=(element+connected_node),length=math_length)
                self._lines[connected_node+element] = Line(label=(connected_node+element),length=math_length)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        plt.figure(figsize=(10, 8))
        # Plot nodes
        for node_label, node in self._nodes.items():
            x, y = node.position
            plt.scatter(x, y, color='blue', s=200)  # Plot node
            plt.text(x, y, node_label, fontsize=20, ha='left')  # Add label next to the node

        # Plot lines between nodes
        for line_label, line in self._lines.items():
            node1_label, node2_label = line_label[0], line_label[1]  # Get node labels from line label
            node1, node2 = self._nodes[node1_label], self._nodes[node2_label]

            # Draw a line between the positions of the two connected nodes
            x_values = [node1.position[0], node2.position[0]]
            y_values = [node1.position[1], node2.position[1]]
            plt.plot(x_values, y_values, color='gray', linewidth=3,
                     label="Line" if line_label == list(self._lines.keys())[0] else "")

        # Show plot with legend and grid for clarity
        plt.legend(loc="upper right")
        plt.grid(True)
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.title("Network Topology")
        return plt.show()

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2, path=None):
        if path is None:
            path = ""
        # Aggiungi il nodo corrente al percorso
        path = path + label1  # Crea una nuova lista per evitare effetti collaterali con la ricorsione
        # Se siamo arrivati al nodo di destinazione, ritorna il percorso trovato
        if label1 == label2:  # Se siamo arrivati al nodo di destinazione, ritorna il percorso trovato
            return [path]  # Ritorna il percorso come lista annidata
        if len(path) > len(self._nodes):  # Se superiamo il numero di nodi, usciamo
            return
        if (label1 or label2) not in self._nodes:
            return print("node not present in the network")

        final_paths = []  # Lista per contenere tutti i percorsi trovati
        # Itera su ogni nodo adiacente
        for next_node in self._nodes[label1].connected_nodes:
            # Verifica che il nodo non sia già nel percorso per evitare cicli
            if next_node not in path:
                # Chiama ricorsivamente la funzione per ogni nodo adiacente
                new_paths = self.find_paths(next_node, label2, path)
                for p in new_paths:
                    final_paths.append(p)
        return final_paths

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        for element in self._nodes:
            for connected_node in self._nodes[element].connected_nodes: #per tutti i nodi vicini
                line_label = element+connected_node #creo la label della linea
                if line_label in self._lines:
                    self._nodes[element].successive[line_label] = self._lines[line_label] #update successive del nodo
                    self._lines[line_label].successive[connected_node] = self._nodes[connected_node]


    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        start_node = signal_information.path[0]
        if start_node in self._nodes:
            self._nodes[start_node].propagate(signal_information)
        return signal_information  # Segnale aggiornato dopo la propagazione
