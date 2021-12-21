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
    
    def set_signals(self):
        pass

    @classmethod
    def get_next(self, t):
        self.construct(self, t)
        self.incr_flow(self)
        self.set_signals(self)
        self.cook_state_from_books(self)
        return self.state