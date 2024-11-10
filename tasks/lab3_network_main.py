import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from docutils.nodes import label
from core.elements import Network, Signal_information, Node

# Exercise Lab3: Network

# Load the Network from the JSON file,
ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'

my_network = Network(file_input) #carica il file json in NETWORK
my_network.connect() #Connette i nodi e le linee riempiendo i rispettivi dizionari "successive"
Network.draw(my_network) #disegna la rete

#istanza delle informazioni che voglio mantenere
latency = []
total_noise = []
SNR = []
path_totali = []

#for annidato per trovare tutte le possibile coppie di nodi partenza/arrivo
nodes_labels = list(my_network.nodes.keys())
number_of_nodes = len(my_network.nodes)
possible_couple = []
for i in range(number_of_nodes):
    for j in range(i+1,number_of_nodes):
        possible_couple.append([nodes_labels[i],nodes_labels[j]])
        possible_couple.append([nodes_labels[j], nodes_labels[i]])

#propagazione lungo la rete di tutti i possibili percorsi
for couple in possible_couple:
    paths = my_network.find_paths(couple[0], couple[1])
    for path in paths:
        # istnaza della potenza del segnale [W]
        input_signal = Signal_information(signal_power=1, path=path)
        my_network.propagate(input_signal)
        #aggiornamento di tutte le info dopo la propagazione
        SNR_int = 10*np.log10(input_signal.signal_power/input_signal.noise_power)
        SNR.append(SNR_int)
        total_noise.append(input_signal.noise_power)
        latency.append(input_signal.latency)
        path_totali.append(path)


#Panda DataFrame con tutti i risultati
df = pd.DataFrame({
    'Path': path_totali,
    'Latency': latency,
    'Noise Power': total_noise,
    'SNR': SNR
})

df.to_csv('Possible_paths_analysys.csv') #csv file del panada dataframe
print(df)








