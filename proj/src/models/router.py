import utils as utils

class Router:
  def __init__(self, cell, range_, cost, coverage):
    
    from models.map import Map # lazy import to avoid circular dependency
    
    self.cell = cell
    self.range_ = range_
    self.cost = cost
    self.coverage = coverage

  def __str__(self):
    return "[" + str(self.cell) + ", " + str(self.cost) + ", " + str(self.range_) + "]"

  def __repr__(self):
    return str(self)  
  
  def __eq__(self, other):
    if isinstance(other, Router):
        return self.cell == other.cell
    return False
  
  def __hash__(self):
    return hash((self.cell, self.range_, self.cost))
