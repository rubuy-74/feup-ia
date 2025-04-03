import models.map as mapClass
import operators.add as add
import operators.remove as remove
from models.solution import Solution
import random

def mutation_func(m: mapClass.Map,
                  solution: Solution,
                  add_rate: float = 0.40,
                  remove_rate: float = 0.40,
                  nothing_rate: float = 0.20):
  
  action = random.choices(["add","remove","nothing"],weights=[add_rate*100,remove_rate*100,nothing_rate*100])[0]

  # do nothing
  if action == "nothing": 
    return solution

  # adds a new router and path to solution
  if action == "add":
    # print("adding")
    return add.add(solution,m)

  # remove random path from the solution
  if action == "remove":
    # print("remving")
    return remove.remove(solution)

  return solution


def crossover_func(first: Solution, second : Solution) -> Solution:
  pass
  