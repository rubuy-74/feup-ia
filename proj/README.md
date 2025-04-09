# IART 2025 - ROUTER PLACEMENT

## How to Run

Due to the implementation of configuration files, running any map with any algorithm is simpler.

In a configuration file, you can: 
- Set which map and algorithm you want to run.
- Set the probabilites of each operator of the mutation function.
- Set a budget constraint to the naive solution.
- Set the map size inside the GUI

```yaml
algorithm: <name of the algorithm>
map: <name of the map>
size: 1
seed: <random integer>
probabilities:
  remove: <desired percentage (decimal)>
  add: <desired percentage (decimal)>
  nothing: <desired percentage (decimal)>
constraints:
  budget: <desired percentage (decimal)>
```
Any custom configuration file must be placed inside the <code>configs</code> folder.

It is important to state that the sum of the three probabilities (add, remove and nothing) must add to 1.

To start the program, run on the <code>src</code> directory:

<code>python3 main.py \<config name> </code>

After the command above, a new window will open with the choosen map and the algorithm will start running **indefinetly** (excl. simulated annealing).

To stop the execution, open the map window and press <code>Space</code>. The execution will stop and the last computed solution will be drawn and dumped into a file in the <code>output</code> folder, as well as a plot.



## The Approach
### Heuristics

Heuristics are employed to guide the search for better solutions. Some heuristics that we used to base off our solution are:
+ Coverage Maximization: Prioritize placing routers in positions which maximize the coverage
+ Minimize Cost: Try to keep routers closer to the backbone to spend less on backbone cells
+ Avoid walls: Ensure that the router placement algorithm do not position routers within walls, to maintain feasibility.

### Evaluation Function

The evaluation function is used to score potential solutions based on their effectiveness and cost. The function is defined by:

**score = 1000\*t + (B - (N * Pb + M * Pr))**

t  - number of targeted cells \
B  - budget \
N  - Number of cells connected to backbone \
Pb - price of connecting one cell to the backbone \
M  -  Number of routers connected to backbone \
Pr - price of connecting a router to the backbone 

This function prioritizes the coverage over the price of the final solution. The contribution of the solution cost penalizes excessive resources.

### Operators:

+ Mutation: Randomly adjust the placement to explore new solutions.
  + Add: Add router in a random position if the budget allows
  + Remove: Removes a random router and its path to the backbone, while maintaining the connection for affected and adjacent routers.
+ Crossover: Combined two solutions to generate a new one.
  + Choose random rectangles in one of the parents. Copy all the squares on the grid from the other solution to the original. The square is of fixed sized.
  + This approach allows the merger of the solutions with a limited amount of calculations for new paths, which can simplifies the calculations. 

## Implemented Algorithms 
### BFS - Breadth First Search
### Greedy Solution (Naive Solution)
### HillClimb
### Simulated Annealing
### Genetic Algorithm

## Parameterizations


## Specification of the Problem

Typically, buildings are connected to the Internet using a fiber backbone. In order to provide wireless Internet access, wireless routers are placed around the building and connected using fiber cables to the backbone.

Given a building plan, the objective is to decide where to put wireless router and how to connect them to the fiber backbone to maximize coverage and minimize cost (not surpassing the budget).

The problem is represented as grid, where each cell can be either a wall cell, a target cell or a void cell. Target cells are cells in which we need to have wireless coverage and the void cells don't need to be covered.

Routers have a limited square of coverage and cannot be placed in wall cells. Backbones in the other hand can be placed anywhere on the grid.

## Related Work

These are related research and solutions to the problem at hand:

+ Principled Modeling of the Google Hash Code Problems for Meta-Heuristics
  + https://estudogeral.uc.pt/retrieve/265403/tese_final_pedro_rodrigues.pdf
+ Genetic algorithms and greedy-randomized adaptive search procedure for router placement problem in wireless networks
  + https://journals.sagepub.com/doi/full/10.3233/JHS-190616
+ Teams Gyrating Flibbittygibbitts solution
  + https://github.com/sbrodehl/HashCode

## Problem Formulation

#### Solution Representation

+ Array of array containing the path for each router
+ Number of non router cells connected to the backbone (N)
+ Number of routers (M)
+ Number of targeted cells covered (t)

#### Mutation Function

+ For any router, choose one of the adjacent cells or the router itself that are not in the path to the backbone
+ If there is budget available, place the router in the chosen cell and replace the previous with a cell connecting to the backbone or no cell at all
+ If there is budget available for a new router, it may place that router
+ There is also a possibility of removing a router and its path

#### Crossover Function

+ Divide the number of routers by two and choose the first half for each
+ For a solution A with Ra routers and another solution B with Rb routers, the child C will have Ra/2 + Rb/2 routers

#### Hard Constraints

+ A router must be placed within the boundaries of the walls
+ There is no wall inside the smallest enclosing rectangle of a cell with a router and a cell that is covered
+ Routers can only be connected to a cell that is already connected to the fiber backbone
+ The maximum spend on routers and backbone is B
+ Routers cannot be placed on walls, but the initial backbone cell can be of any type (target,void or wall cell)

#### Evalutation Functions

**score = 1000\*t - (B - (N * Pb + M * Pr))**

t  - number of targeted cells \
B  - budget \
N  - Number of cells connected to backbone \
Pb - price of connecting one cell to the backbone \
M  -  Number of routers connected to backbone \
Pr - price of connecting a router to the backbone 

## Implementation

+ The language which will be used is Python
+ The IDE used will be VScode
+ The version control system is Git with Github

### Data Structures

+ Grid
+ Router
+ Solution
+ Position