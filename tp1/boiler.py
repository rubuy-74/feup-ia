class BucketState:
    c1 = 4
    c2 = 3
    
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.b1, self.b2)) 

    def __str__(self):
        return "(" + str(self.b1) + ", " + str(self.b2) + ")"
    
# emptying the first bucket
def empty1(state):
    if state.b1 > 0:
        return BucketState(0, state.b2)
    return None

# emptying the second bucket
def empty2(state):
    # your code here
    

# your code here