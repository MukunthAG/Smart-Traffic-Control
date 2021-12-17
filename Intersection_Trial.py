import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import numpy as np
from graph_funcs_trial import *

NO_OF_MODS = None
MAIN_LANES = 4

# GRAPH 

G = nx.DiGraph()

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
shape = nx.spring_layout(G, k=1)
node_color_map = extract_values("color", node_attrs)

# ANIMATION

pf_node_attrs = node_attrs # Previous frame property initialized with default value
pf_edge_attrs = edge_attrs

def updater(t, shape, ax):
    ax.clear()
    """
    READ the global variables: G, shape, node_color
    MODIFY (So, UPDATE) the global variables: pf_node_attrs, pf_edge_attrs

    Its okay to get out of the scope because we are "Changing" only two variables

    """
    global pf_node_attrs
    global pf_edge_attrs

    # TESTING READ
    flow_rates = extract_values("flow_rate", node_attrs)

    # TESTING WRITE
    cur_node_attrs = pf_node_attrs
    cur_edge_attrs = pf_edge_attrs

    def opa_func(t, period = 10):
        t = shrink_interval(t, period)
        opa = None
        if t <= 5: opa = (5 - t)/5
        else: opa = (t - 5)/5
        return opa
    
    for node in cur_node_attrs:
        if node["direction"] == "I":
            node["density"] = opa_func(t)
    
    opacities = extract_values("density", cur_node_attrs)

    nx.draw_networkx_nodes(G, pos = shape, node_color = node_color_map, alpha = opacities)
    nx.draw_networkx_labels(G, shape)
    nx.draw_networkx_edges(G, shape)

    ax.set_title("Frame {}".format(t))
    pf_node_attrs = cur_node_attrs
    pf_edge_attrs = cur_edge_attrs

anim_window, anim_axes = plt.subplots()
anim_setup = {
    "fig": anim_window,
    "frames": np.arange(0,30,0.5),
    "interval": 500,
    "fargs" : (shape, anim_axes)
}
anim_data = animate(func = updater, **anim_setup)
anim_data.save('sample.gif')

plt.show()