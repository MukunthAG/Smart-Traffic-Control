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
    def read_previous(self):
        return self.prev_state

class State(PrevState):
    time = 0

    def construct(self, t, G):
        self.graph_state = self.read_previous()
        self.time = t
        self.type = get_nvalues(G, "type")
        self.traf_state = self.graph_state["alpha"]
        self.sig_state = self.graph_state["edge_color"]
        self.flow_rates = self.graph_state["flow_rates"]
    
    def incr_flow(self):
        for i, (type, alpha, flow_rate) in enumerate(zip(self.type, self.traf_state, self.flow_rates)):
            if type == "I":
                alpha += flow_rate
                if alpha > 1: 
                    alpha = 1
            self.traf_state[i] = alpha
        self.graph_state["alpha"] = self.traf_state

    def new_state(self):
        self.incr_flow(self)
        return self.graph_state

    @classmethod
    def get_next(self, t, G):
        self.construct(self, t, G)
        new_state = self.new_state(self)
        self.update(new_state)
        return new_state