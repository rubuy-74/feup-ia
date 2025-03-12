<!-- # IART 2024 - Router Placement -->
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

### Current Solutions

+ Greedy - using the closest possible target cell where there is no coverage from another router