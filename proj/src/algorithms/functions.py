from models.map import Map
import operators.add as add
import random

def mutation_func(m: Map,
                  current_budget: int,
                  add_rate: float,
                  remove_rate: float,
                  nothing_rate: float):
  
  action = random.choices(["add","remove","nothing"], weights=[add_rate*100,remove_rate*100,nothing_rate*100])[0]

  # do nothing
  if action == "nothing": 
    return m, current_budget, "noth"

  # adds a new router and path to solution
  if action == "add":
    return add.add(m, current_budget)

  # remove random path from the solution
  if action == "remove":
    return add.remove(m, current_budget)
    

  return m, current_budget, "noth"
  