import numpy as np
import pprint as pp
from graph_funcs import get_nvalues, get_evalues

FRAME_INTERVAL = 1000 #ms

def gen_frames():
    np.arange(0, 10, 1)

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
    traf_state = None
    sig_state = None
    flow_rates = None

    @classmethod
    def fetch(self, graph_state):
        self.traf_state = graph_state["alpha"]
        self.sig_state = graph_state["edge_color"]
        self.flow_rates = graph_state["flow_rates"]
        new_state = self.new_state()
    
    def new_state(self):
        pass