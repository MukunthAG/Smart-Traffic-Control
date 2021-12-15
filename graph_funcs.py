import numpy as np
import pprint as pp

TEST_MODE = 0

#Standard Make-it-Easy Functions

def Range(start_num, end_num):
    return range(start_num, end_num + 1)

def Pretty(any):
    return pp.pprint(any)

#Local Functions

def to_vp10ms(num): # Convert to Vehicles per 10 milliseconds
    return (num/3600)*0.01

def inflow_gen(n, lane_group):
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
            
#Global Functions

def lane_nodes(n, direction):
    lane_nodes = []
    for i in Range(1, n):
        current_lane_group = i
        node_attributes = {
            "color": "pink",
            "direction": direction,
            "lane_group" : current_lane_group,
        }
        if direction == "I":
            node_attributes["flow_rate"] = inflow_gen(n, current_lane_group)
            node_attributes["color"] = "blue"
        node = [direction + str(current_lane_group), node_attributes]
        lane_nodes.append(tuple(node))
    return lane_nodes

def mod_nodes(n, id):
    return [(id, {"color": "yellow", "congestion": None})]

#Testing 

if TEST_MODE == 1:
    Pretty(lane_nodes(4, "O"))
