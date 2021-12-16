import numpy as np
import pprint as pp

TEST_MODE = 0

# Standard Make-it-Easy Functions

def Range(start_num, end_num):
    return range(start_num, end_num + 1)

def Pretty(any):
    return pp.pprint(any)

# CONSTRUCT GRAPH

"""
Create Nodes (Semi Custom)--> Initialize with name (gen), color (static), type (static), flow_rate (gen), *density (dynamic)
Create Edges (Semi Custom)--> Initialize with name (gen), *color (dynamic), from reading the node_props list 
Create Graph --> Add Nodes and Edges, and Maybe SubGraphs
Write a Draw function --> Draw Nodes, Edges and Labels
"""