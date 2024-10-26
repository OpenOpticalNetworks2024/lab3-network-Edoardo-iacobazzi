import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from core.elements import Node, Network, Signal_information

# Exercise Lab3: Network

# Load the Network from the JSON file,
ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'


#connect nodes and lines in Network.

# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
my_network = Network(file_input)
Network.draw(my_network)

print(my_network.nodes)
print(my_network.lines)

# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file







