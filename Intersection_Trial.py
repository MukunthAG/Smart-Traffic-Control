import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import numpy as np
from graph_funcs import *

NO_OF_MODS = None
MAIN_LANES = 4

# GRAPH 

G = nx.Graph()

mod_node = mod_nodes(NO_OF_MODS, "M")
in_nodes = lane_nodes(MAIN_LANES, "I")
out_nodes = lane_nodes(MAIN_LANES, "O")

G.add_nodes_from(mod_node)
G.add_nodes_from(in_nodes)
G.add_nodes_from(out_nodes)

edge_bunch = create_edges_trial(G)
G.add_edges_from(edge_bunch)

node_attrs = [G.nodes[node] for node in G.nodes]
edge_attrs = [G.edges[edge] for edge in G.edges]
shape = nx.spring_layout(G)
node_color_map = [node_dict["color"] for node_dict in node_attrs]

# EXTRACTED DATA TO BE MODIFIED

opacities = [node_dict["density"] for node_dict in node_attrs]
signals = [edge_dict["color"] for edge_dict in edge_attrs]

# ANIMATION

pframe_opa = opacities # Previous frame property initialized with default value
pframe_sig = signals

def updater(t):
    """
    READ the global variables: G, shape, node_color
    MODIFY (So, UPDATE) the global variables: pframe_opa, pframe_sig

    Its okay to get out of the scope because we are "Changing" only two variables

    """
    global pframe_opa
    global pframe_sig

    
    nx.draw(G, pos = shape, node_color = node_color_map, alpha = opacities, edge_color = signals, with_labels = True)

anim_window, ax = plt.subplot()
anim_setup = {
    "fig": anim_window,
    "frames": None,
    "interval": None
}
anim_data = animate(func = updater,**anim_setup)

plt.show()