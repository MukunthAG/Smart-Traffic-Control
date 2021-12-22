import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animate
from graph_funcs import *
from anim_funcs import *

# MAIN UPDATE FUNCTION

def frame_updater(t, G, anim_axes):
    anim_axes.clear()
    graph_state = State.get_next(t)
    Draw(G, **graph_state)
    anim_axes.set_title("Time:{}".format(t))

# INITIALIZE GRAPH

G = nx.Graph()

node_list = create_nodes()
edge_list = create_edges(node_list)
G.add_nodes_from(node_list)
G.add_edges_from(edge_list)
update_additional_attrs(G)

graph_setup = {
    "pos": nx.kamada_kawai_layout(G),
    "node_color": get_nvalues(G, "color"),
    "node_size": get_nvalues(G, "node_size"),
    "alpha": get_nvalues(G, "opacity"),
    "flow_rates": get_nvalues(G, "flow_rate"),
    "edge_color": get_evalues(G, "color"),
    "width": get_evalues(G, "width"),
    "with_labels": True, 
    "font_size": 8
}

State.initialize(G, graph_setup)

# ANIMATE GRAPH

anim_window, anim_axes = plt.subplots()
anim_setup = {
    "fig": anim_window,
    "func": frame_updater,
    "interval": FRAME_INTERVAL,
    "frames": np.arange(0, TOTAL_FRAMES, 1),
    "fargs": (G, anim_axes),
    "repeat": False
}
anim_data = animate(**anim_setup)
anim_data.save("Basic_Model_simul_10min.gif")

# SHOW GRAPH

plt.show()

