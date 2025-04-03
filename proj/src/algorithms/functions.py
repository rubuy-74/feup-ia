from models.map import Map
import operators.add as add
import operators.remove as remove
import random

def mutation_func(m: Map,
                  add_rate: float = 0.40,
                  remove_rate: float = 0.40,
                  nothing_rate: float = 0.20):
  
  action = random.choices(["add","remove","nothing"], weights=[add_rate*100,remove_rate*100,nothing_rate*100])[0]

  # do nothing
  if action == "nothing": 
    return m

  # adds a new router and path to solution
  if action == "add":
    return add.add(m)

  # remove random path from the solution
  if action == "remove":
    print("remving")
    

  return m
  