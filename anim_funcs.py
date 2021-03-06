import numpy as np
import pprint as pp
from graph_funcs import Pretty, get_nvalues, get_evalues
from constants import *

class PrevState:
    state = None
    node_book = None
    edge_book = None

    @classmethod
    def initialize(self, G, state):
        self.state = state
        self.node_book = [G.nodes[node] for node in G.nodes]
        self.edge_book = [G.edges[edge] for edge in G.edges]

class State(PrevState):

    def construct(self, t):
        self.time = t
        for node in self.node_book:
            if node["type"] == "M":
                node["time"] += 1
    
    def incr_flow(self):
        for node in self.node_book:
            opacity = node["opacity"]
            if node["type"] == "I":
                opacity += node["flow_rate"]
                if opacity > 1: opacity = 1
            node["opacity"] = opacity
    
    def set_signals(self):
        self.change_phase(self)
        self.trigger_check(self)
    
    def release_flow(self): 
        for node in self.node_book:
            opacity = node["opacity"]
            if node["type"] == "I" and node["triggered"] == True:
                opacity -= RELEASE_RATE
                if opacity < 0: opacity = 0
                if opacity > 1: opacity = 1
            node["opacity"] = opacity
    
    def cook_state_from_books(self):
        self.state.update({
            "alpha": [node["opacity"] for node in self.node_book],
            "edge_color": [edge["color"] for edge in self.edge_book]
        })

    def change_phase(self):
        for node in self.node_book:
            if node["type"] == "M" and node["triggered"] == True:
                self.parent_node_name = node["name"]
                self.largest_I_density = -np.Inf
                self.largest_I_density_name = None
                for edge in self.edge_book:
                    if edge["edge_end"] == self.parent_node_name:
                        I_name = edge["edge_start"]
                        I_density = self.get_attr_with_name(
                            self, "opacity", I_name
                        )
                        self.record_flows(self, I_density, I_name)
                self.set_colors(self, self.largest_I_density_name)
                node["active_node"] = self.largest_I_density_name
                node["triggered"] = False

    def trigger_check(self):
        for node in self.node_book:
            if node["type"] == "M":
                active_node = node["active_node"]
                active_density = self.get_attr_with_name(
                    self, "opacity", active_node
                )
                if (
                    active_density <= THRESHOLD_DENSITY_FOR_CLEARANCE 
                    or 
                    node["time"] >= TOLERATABLE_WAIT_TIME
                   ):
                    node["triggered"] = True
                    node["time"] = 0  

    def get_attr_with_name(self, attr, name):
        node_attr = None 
        for node in self.node_book:
            if node["name"] == name:
                node_attr = node[attr]
        return node_attr    

    def record_flows(self, I_density, I_name):
        if I_density > self.largest_I_density:
            self.largest_I_density = I_density
            self.largest_I_density_name = I_name
    
    def set_colors(self, I_name):
        for node in self.node_book:
            I_group_id = self.get_attr_with_name(
                self, "group_id", I_name
            )
            if node["parent"] == self.parent_node_name:          
                if (
                    (node["group_id"] == I_group_id and node["type"] == "I") 
                        or 
                    (node["group_id"] != I_group_id and node["type"] == "O")
                   ):
                    for edge in self.edge_book:
                        if (
                            self.edge_is_between(
                                self, edge, self.parent_node_name, node["name"])
                            ):
                            edge["color"] = "green"
                            node["triggered"] = True
                else:
                    for edge in self.edge_book:
                        if (
                            self.edge_is_between(
                                self, edge, self.parent_node_name, node["name"])
                            ):
                            edge["color"] = "red"
                            node["triggered"] = False       
    
    def edge_is_between(self, edge, n1, n2):
        if (
            edge["edge_start"] == n1 and
            edge["edge_end"] == n2
           ):
           return True
        if (
            edge["edge_start"] == n2 and
            edge["edge_end"] == n1
           ): 
           return True
        return False
 
    @classmethod
    def get_next(self, t):
        self.construct(self, t)
        self.incr_flow(self)
        self.set_signals(self)
        self.release_flow(self)
        self.cook_state_from_books(self)
        return self.state