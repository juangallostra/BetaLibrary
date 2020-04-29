import random as rn
import uuid

class IDGenerator():
    def __init__(self, seed=0):
        self._seed = seed
        self.rd = rn.Random()
        self.rd.seed(0)
    
    def next_id(self):
        return str(uuid.UUID(self.rd.getrandbits(128)))
