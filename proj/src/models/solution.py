import utils as utils
import models.router as router

class Solution:
  def __init__(self,paths : dict, routers : set):
    self.routers = routers
    self.paths = paths
    self.n = len(routers)
    self.m = getPathsLength(paths)
    self.t = calculateTargets(routers) 

  def __str__(self):
    return f"[{str(self.routers)},{str(self.paths)},{str(self.n)},{str(self.m)},{str(self.t)}]"

  def getTargets(self):
    targets = map(lambda router: router.targets,self.routers)
    return [x for xs in targets for x in xs]
  
def calculateTargets(routers : list[router.Router]) -> int:
  targetList : list[int] = list(map(lambda router: len(router.targets),routers))
  return sum(targetList)

def getPathsLength(paths : dict) -> int:
  values = []
  for _,v in paths.items():
    values.append(len(v))
  return sum(values)
