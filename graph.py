import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animate
from graph_funcs import *
from anim_funcs import *

# MAIN UPDATE FUNCTION

def frame_updater():
    pass

# INITIALIZE GRAPH

G = nx.Graph()

node_list = create_nodes()
edge_list = create_edges(node_list)
G.add_nodes_from(node_list)
G.add_edges_from(edge_list)

graph_setup = {
    "pos": nx.kamada_kawai_layout(G),
    "node_color": get_nvalues(G, "color"),
    "node_size": get_nvalues(G, "node_size"),
    "alpha": get_nvalues(G, "opacity"),
    "edge_color": get_evalues(G, "color"),
    "width": get_evalues(G, "width"),
    "with_labels": True, 
    "font_size": 8
}

Draw(G, **graph_setup)

# ANIMATE GRAPH

"""
anim_window, anim_axes = plt.subplots()
anim_setup = {
    "fig": anim_window,
    "func": frame_updater,
    "interval": FRAME_INTERVAL,
    "frames": gen_frames(),
    "fargs" : None # For Now
}
anim_data = animate(**anim_setup)
"""

# SHOW GRAPH

plt.show()