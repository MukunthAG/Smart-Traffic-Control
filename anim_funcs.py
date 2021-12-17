import numpy as np
import pprint as pp
from graph_funcs import get_nvalues, get_evalues

FRAME_INTERVAL = 1000 #ms

class PrevState:
    prev_state = None

    @classmethod
    def update(self, state):
        self.prev_state = state
        pass

    @classmethod
    def read(self):
        return self.prev_state

def gen_frames():
    np.arange(0, 10, 1)