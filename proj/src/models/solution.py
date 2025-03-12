import utils as utils

class Solution:
  def __init__(self,paths : dict, routers :list):
    self.routers = routers
    self.paths = paths
    self.n = len(routers)
    self.m = utils.getPathsLength(paths)
    self.t = utils.calculateTargets(routers) 

  def __str__(self):
    return f"[{str(self.routers)},{str(self.paths)},{str(self.n)},{str(self.m)},{str(self.t)}]"