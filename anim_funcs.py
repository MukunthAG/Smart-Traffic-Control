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
    
    def cook_state_from_books(self):
        self.state.update({
            "alpha": [node["opacity"] for node in self.node_book],
            "edge_color": [edge["color"] for edge in self.edge_book]
        })

    def incr_flow(self):
        for node in self.node_book:
            opacity = node["opacity"]
            if node["type"] == "I":
                opacity += node["flow_rate"]
                if opacity > 1: opacity = 1
            node["opacity"] = opacity
    
    def record_flows(self, I_density, I_name):
        if I_density > self.largest_I_density:
            self.largest_I_density = I_density
            self.largest_I_density_name = I_name
    
    def get_attr_with_name(self, attr, name):
        node_attr = None 
        for node in self.node_book:
            if node["name"] == name:
                node_attr = node[attr]
        return node_attr
    
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
        
    def set_colors(self):
        for node in self.node_book:
            I_group_id = self.get_attr_with_name(
                self,
                "group_id", 
                self.largest_I_density_name
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
                else:
                    for edge in self.edge_book:
                        if (
                            self.edge_is_between(
                                self, edge, self.parent_node_name, node["name"])
                            ):
                            edge["color"] = "red"

    def set_signals(self):
        for node in self.node_book:
            if node["type"] == "M":
                self.parent_node_name = node["name"]
                self.largest_I_density = -np.Inf
                self.largest_I_density_name = None
                for edge in self.edge_book:
                    if edge["edge_end"] == self.parent_node_name:
                        I_name = edge["edge_start"]
                        I_density = self.get_attr_with_name(self, "opacity", I_name)
                        self.record_flows(self, I_density, I_name)
                self.set_colors(self)
                
    @classmethod
    def get_next(self, t):
        self.construct(self, t)
        self.incr_flow(self)
        self.set_signals(self)
        self.cook_state_from_books(self)
        return self.state