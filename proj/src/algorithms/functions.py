import models.map as mapClass
import models.solution as solution
import operators.add as add
import operators.shift as shift
import operators.remove as remove
import random

def mutation_func(m: mapClass.Map,
                  solution: solution.Solution,
                  change_rate: float = 0.0,
                  add_rate: float = 0.5,
                  remove_rate: float = 0.5,
                  nothing_rate: float = 0):
  
  action = random.choices(["change","add","remove","nothing"],weights=[change_rate*100,add_rate*100,remove_rate*100,nothing_rate*100])[0]

  # do nothing
  if action == "nothing": 
    return solution

  # adds a new router and path to solution
  if action == "add":
    print("adding")
    return add.add(solution,m)

  # remove random path from the solution
  if action == "remove":
    print("remving")
    return remove.remove(solution,m)

  # change router position and update path
  if action == "change":
    return shift.shift(solution, m)

  return solution


def crossover_func():
  pass