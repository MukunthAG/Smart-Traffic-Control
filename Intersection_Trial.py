import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from graph_funcs import *

NO_OF_MODS = None
MAIN_LANES = 4

G = nx.Graph()

mod_node = mod_nodes(NO_OF_MODS, "M")
in_nodes = lane_nodes(MAIN_LANES, "I")
out_nodes = lane_nodes(MAIN_LANES, "O")

G.add_nodes_from(mod_node)
G.add_nodes_from(in_nodes)
G.add_nodes_from(out_nodes)

node_attrs = [G.nodes[node] for node in G.nodes]
init_color_map = [node_dict["color"] for node_dict in node_attrs]
edge_bunch = create_edges_trial(G)

G.add_edges_from(edge_bunch)

shape = nx.spring_layout(G)
nx.draw(G, pos = shape, with_labels = True, node_color = init_color_map)

plt.show()