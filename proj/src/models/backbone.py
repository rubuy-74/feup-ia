class Backbone:
  def  __init__(self, cell, cost):
      self.cell = cell
      self.cost = cost
      self.connected_to = set()
      
  def __str__(self):
    return "[" + str(self.cell) + ", " + str(self.cost) + ", " + str(self.connected_to) + "]"  