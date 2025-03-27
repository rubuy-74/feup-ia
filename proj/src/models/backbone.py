import utils as utils
class Backbone:
  def  __init__(self, cell, cost):
      self.cell = cell
      self.cost = cost
      self.connections = {}
      
  def __str__(self):
    return "[" + str(self.cell) + ", " + str(self.cost) + ", " + str(self.connections) + "]"

  def getConnectionsAsSet(self):
      return utils.convertDictToSet(self.connections)