import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from core.elements import Node


# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'


# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file

#lettura file json
with open( file_input ,'r') as file:
    data = json.load(file)

print(data)
nodes = list()
for k,v in data.items():
    nodes.append(Node(label=k,position=v['position'],connected_nodes=v['connected_nodes']))

print(nodes)

print(nodes[0].label)