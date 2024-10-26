import json
import matplotlib.pyplot as plt
import numpy as np
from blinker import signal
from networkx.algorithms.bipartite.basic import color

from core.parameters import c

# from core.utils import example_fun() questo per importare una classe da un altro file


class Signal_information(object):
    def __init__(self,signal_power,path): #constructor
        self._signal_power = signal_power
        self._latency = 0
        self._noise_power = 0
        self._path = path

    @property
    def signal_power(self): #property
        return self._signal_power

    def update_signal_power(self,added_value):
        self._signal_power = self.signal_power + added_value

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
        if len(self.path) < 0:
            self._path = self._path[1:]


class Node(object):     #defiito da un dizionario letto dal file json in Network
    def __init__(self,label,position, connected_nodes):
        self._label = label
        self._position = position
        self._connected_nodes = connected_nodes
        self._successive = {}

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

        signal_information.update_path()
        self.successive[signal_information.path[0]+signal_information.path[1]].propagate(signal_information)



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

        self.successive[signal_information.path[0]].propagate(signal_information)
       

class Network(object):
    def __init__(self,file_in):
        self._nodes = {}
        self._lines = {}

        with open( file_in ,'r') as file:
            data = json.load(file)

        for element in data:
            self._nodes[element] = Node(label=element,position=data[element]["position"],connected_nodes=data[element]["connected_nodes"])

        for element in self._nodes:
            for connected_node in self._nodes[element].connected_nodes:
                #distanza euclidea con numpy
                print(self.nodes[connected_node].position[0])
                punto_a = np.array(self.nodes[connected_node].position)
                punto_b = np.array(self.nodes[element].position)
                math_length = np.linalg.norm(punto_a - punto_b)
                self._lines[element+connected_node] = Line(label=(element+connected_node),length=math_length)
                self._lines[connected_node+element] = Line(label=(connected_node+element),length=math_length)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        for element in self._nodes:
            plt.scatter(self.nodes[element].position[0], self.nodes[element].position[1], color='blue')

        return plt.show()



    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2, path=None):
        pass
    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
       pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        start_node_label = signal_information.path[0]
        if start_node_label in self._nodes:
            self._nodes[start_node_label].propagate(signal_information)
        return signal_information  # Segnale aggiornato dopo la propagazione
