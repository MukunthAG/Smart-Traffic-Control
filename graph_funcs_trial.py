import numpy as np
import pprint as pp

TEST_MODE = 0

#Standard Make-it-Easy Functions

def Range(start_num, end_num):
    return range(start_num, end_num + 1)

def Pretty(any):
    return pp.pprint(any)

def shrink_interval(var, end):
    res = None
    if var%end == 0 and var != 0: 
        res = end
    elif var == 0:
        res = 0
    else:
        res = var%end
    return res

#Local Functions

def to_vp10ms(num): # Convert to Vehicles per 10 milliseconds
    return (num/3600)*0.01

def inflow_rate_gen(n, lane_group):
    if lane_group <= 0 or lane_group > n:
        raise Exception("Lanes start count from 1 to n!")
    flow_rates = []
    high = 500 # Vehicles per Hour (vph)
    low = 100
    for lane in Range(1, n):
        if lane == 1:
            flow_rates.append(to_vp10ms(high))
        else:
            flow_rates.append(to_vp10ms(low))
    return flow_rates[lane_group - 1]

def edge_width_gen():
    return None
            
#Global Functions

def lane_nodes(n, direction):
    lane_nodes = []
    for i in Range(1, n):
        current_lane_group = i
        node_attributes = {
            "color": "pink",
            "direction": direction,
            "lane_group" : current_lane_group,
            "density": 1,
            "flow_rate": 0
        }
        if direction == "I":
            node_attributes["flow_rate"] = inflow_rate_gen(n, current_lane_group)
            node_attributes["color"] = "blue"
        node = [direction + str(current_lane_group), node_attributes]
        lane_nodes.append(tuple(node))
    return lane_nodes

def mod_nodes(n, id):
    return [(id, {"color": "yellow", "flow_rate": 0, "congestion": None, "direction": None, "density": 1})]

def create_edges_trial(G):
    edges = []
    for node in list(G.nodes): #next try "not in"
        if node != "M":
            edge_attributes = {
                "Color": "black",
                "width": None,
                "direction": "IM"
            }
            edge = (node, "M", edge_attributes)
            if node[0] == "O":
                edge_attributes["direction"] = "MO"
                edge = ("M", node, edge_attributes)
            edges.append(edge)
    return edges   

def extract_values(key, dictofdict):
    return [dict[key] for dict in dictofdict]

#Testing 

if TEST_MODE == 1:
    Pretty(shrink_interval(16.66, 10))
    Pretty(shrink_interval(30, 10))
    Pretty(shrink_interval(0, 10))
