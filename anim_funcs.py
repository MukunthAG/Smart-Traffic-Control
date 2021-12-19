import numpy as np
import pprint as pp
from graph_funcs import Pretty, get_nvalues, get_evalues

FPS = 20
FRAME_INTERVAL = 1000/FPS #ms
TOTAL_FRAMES = 600 + 1

class PrevState:
    prev_state = None

    @classmethod
    def update(self, state):
        self.prev_state = state
        pass

    @classmethod
    def read(self):
        return self.prev_state

class CurrentState:
    time = 0
    graph_state = None

    @classmethod
    def fetch(self, t, G, graph_state):
        self.time = t
        self.type = get_nvalues(G, "type")
        self.graph_state = graph_state
        self.traf_state = graph_state["alpha"]
        self.sig_state = graph_state["edge_color"]
        self.flow_rates = graph_state["flow_rates"]
        new_state = self.new_state(self)
        return new_state
    
    def new_state(self):
        for i, (type, alpha, flow_rate) in enumerate(zip(self.type, self.traf_state, self.flow_rates)):
            if type == "I":
                alpha += flow_rate
                if alpha > 1: 
                    alpha = 1
            self.traf_state[i] = alpha
        self.graph_state["alpha"] = self.traf_state
        return self.graph_state