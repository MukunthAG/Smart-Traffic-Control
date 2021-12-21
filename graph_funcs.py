import networkx as nx
import numpy as np
import pprint as pp
import random
from constants import *

TEST_MODE = 0

# Standard Make-it-Easy Functions

def Range(start_num, end_num):
    return range(start_num, end_num + 1)

def Pretty(any):
    return pp.pprint(any)

def tuples_to_list(array_of_tuples):
    array_of_list = []
    for tuple in array_of_tuples:
        _list = list(tuple)
        array_of_list.append(_list)
    return array_of_list

def lists_to_tuple(array_of_lists):
    array_of_tuple = []
    for list in array_of_lists:
        _tuple = tuple(list)
        array_of_tuple.append(_tuple)
    return array_of_tuple

# CONSTRUCT GRAPH

"""
Create Nodes (Semi Custom)--> Initialize with name (gen), color (static), type (static), flow_rate (gen), 
*density (dynamic), parent (static) etc.

Create Edges (Semi Custom)--> Initialize with name (gen), *color (dynamic), from reading the node_attrs list 

Create Graph --> Add Nodes and Edges, Two major graphs (Intersections) may be linked manually

Write a Draw function --> Draw Nodes, Edges and Labels

Try an Allowance for Pump Nodes and Sink Nodes
"""

# Manual Initialization

"""MODS are nodes at the Intersection, LANE_GROUPS are In and Out Nodes of the same side of Lane"""

NUM_OF_MODS = 4
NUM_OF_LANE_GROUPS = 4

# Create Nodes

def m_gen(m):
    node_attrs = {
        "name": "M{}".format(m),
        "type": "M",
        "intersection_id": m,
        "group_id": None,
        "color": "orange",
        "parent": None,
        "density": None,
        "opacity": 1,
        "node_size": 1000,
        "flow_rate": 0,
        "is_bridge": False,
    }
    node = (node_attrs["name"], node_attrs)
    return node

def i_gen(m, l):
    node_attrs = {
        "name": "I{}{}".format(m,l),
        "type": "I",
        "intersection_id": m,
        "group_id": l,
        "color": "blue",
        "parent": "M{}".format(m),
        "density": None,
        "opacity": 1,
        "node_size": 400,
        "flow_rate": 0,
        "is_bridge": False
    }
    node = (node_attrs["name"], node_attrs)
    return node

def o_gen(m, l):
    node_attrs = {
        "name": "O{}{}".format(m,l),
        "type": "O",
        "color": "pink",
        "intersection_id": m,
        "group_id": l,
        "parent": "M{}".format(m),
        "density": None,
        "opacity": 1,
        "node_size": 400,
        "flow_rate": 0,
        "is_bridge": False
    }
    node = (node_attrs["name"], node_attrs)
    return node

def assign_flow_rates(node_list):
    min = 200 # Vehicle per hour
    max = 600
    max_allowable_limit = MAX_ALLOWABLE_LIMIT_ON_EACH_LANE
    node_list = tuples_to_list(node_list)
    for node in node_list:
        node_attr = node[1]
        if node_attr["type"] == "I":
            vph = random.randint(min, max)
            vps = vph/3600
            max_time = max_allowable_limit/vps
            node_attr["flow_rate"] = 1/max_time # In opacity units
            # Pretty((vph, vps, max_time, 1/max_time))
            node[1] = node_attr
    node_list = lists_to_tuple(node_list)
    return node_list

def init_opacities(node_list):
    node_list = tuples_to_list(node_list)
    for node in node_list:
        node_attr = node[1]
        if node_attr["type"] == "I":
            opacity = random.random()
            node_attr["opacity"] = opacity
            node[1] = node_attr
            # Pretty((0, opacity, 1))
    node_list = lists_to_tuple(node_list)
    return node_list

def create_nodes():
    node_list = [] # node element struct --> (node_name->str, node_attrs->dict)->tuple
    for m in range(0, NUM_OF_MODS):
        node_list.append(m_gen(m))
        for l in range(0, NUM_OF_LANE_GROUPS):
            node_list.append(i_gen(m, l))
            node_list.append(o_gen(m, l))
    node_list = assign_flow_rates(node_list)
    node_list = init_opacities(node_list)
    return node_list

# Create Edges

def assign_edge_width():
    return 1

def create_primary_edges(node_list):
    edge_list = []
    for node_name, node_attrs in node_list:
        if node_attrs["type"] == "M":
            parent_name = node_attrs["name"]
            edge = None
            for node_name, node_attrs in node_list:
                if node_attrs["parent"] == parent_name:
                    edge_attrs = {
                        "name": parent_name + node_name,
                        "color": "black",
                        "type": "primary",
                        "width": assign_edge_width()
                    }
                    if node_attrs["type"] == "I":
                        edge_attrs.update({
                            "edge_start": node_name,
                            "edge_end": parent_name 
                        })
                        edge = (node_name, parent_name, edge_attrs)
                        edge_list.append(edge)
                    if node_attrs["type"] == "O":
                        edge_attrs.update({
                            "edge_start": parent_name,
                            "edge_end": node_name 
                        })
                        edge = (parent_name, node_name, edge_attrs)
                        edge_list.append(edge)
    return edge_list        
            
def create_intersection_edges(node_list): # Creating MANUALY for 4 edges, may be I will automate later😪
    edge_list = [
        ["O00", "I10"],
        ["O10", "I00"],
        ["O11", "I21"],
        ["O21", "I11"],
        ["O20", "I30"],
        ["O30", "I20"],
        ["O31", "I01"],
        ["O01", "I31"]
    ]
    edge_attrs = { # IT WOULD BE BETTER IF EDGE ATTRIBUTES WHERE OUTSIDE
        "name": "Junc", # Need to generate, Pausing for now
        "color": "black",
        "type": "intersection",
        "width": assign_edge_width()
    }
    for edge in edge_list: 
        edge_attrs.update({
            "edge_start": edge[0], 
            "edge_end": edge[1]
        })
        edge.append(edge_attrs)
    edge_list = [tuple(edge) for edge in edge_list]
    return edge_list

def create_edges(node_list):
    primary_edge_list = create_primary_edges(node_list)
    intersection_edge_list = create_intersection_edges(node_list)
    edge_list = primary_edge_list + intersection_edge_list
    return edge_list

def update_additional_attrs(G):
        for node in G.nodes:
            if G.degree[node] == 2:
                nx.set_node_attributes(G, {node: True}, name="is_bridge")

# DRAWING TOOLS 

"""
For various reasons, a manual "Draw" function was required apart from the one by networkx.
Similar reasons for getters of element (nodes and edges) attributes
"""

def Draw(G, **graph_setup):
    gs = graph_setup
    nx.draw_networkx_nodes(
        G, pos = gs["pos"], 
        node_color = gs["node_color"],
        node_size = gs["node_size"],
        alpha = gs["alpha"]
    )
    nx.draw_networkx_edges(
        G, pos = gs["pos"], 
        edge_color = gs["edge_color"],
        width = gs["width"]
    )
    if gs["with_labels"] == True:
        nx.draw_networkx_labels(
            G, pos = gs["pos"],
            font_size = gs["font_size"]
        )

def get_nvalues(G, key):
    values = nx.get_node_attributes(G, key).values()
    return list(values)

def get_evalues(G, key):
    values = nx.get_edge_attributes(G, key).values()
    return list(values)

# TESTING 
    
if TEST_MODE == 1:
    node_list = create_nodes()
    Pretty(node_list)
    Pretty(create_primary_edges(node_list))
    Pretty(create_intersection_edges(node_list))
    Pretty(create_edges(node_list))
    