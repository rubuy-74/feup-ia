import models.map as mapClass
import models.solution as solution
import operators.add as add
import random

def mutation_func(map: mapClass.Map,
                  solution: solution.Solution,
                  change_rate: float = 0.25,
                  add_rate: float = 0.25,
                  remove_rate: float = 0.25,
                  nothing_rate: float = 0.25):
  
  action = random.choices(["change","add","remove","nothing"],weights=[change_rate*100,add_rate*100,remove_rate*100,nothing_rate*100])

  # do nothing
  if action == "nothing": return

  # adds a new router and path to solution
  if action == "add":
    return add.add(solution,map)

  # remove random path from the solution
  if action == "remove":
    # TODO
    #return remove.remove(solution,map)
    pass

  # change router position and update path
  if action == "change":
    #TODO
    #return change.change(solution,map)
    pass

  return


def crossover_func():
  pass

def evaluation_func(map: mapClass.Map, solution: solution.Solution):
  return 1000 * solution.t + ( map.budget - ( solution.m * map.bbPrice + solution.n * map.rtPrice ) )