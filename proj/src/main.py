import sys
import pygame
import ctypes
import utils as utils
import algorithms.randomSolution as randomSolution
import algorithms.greedySolution as greedySolution

""" def find_nearest_available_cell_to_router(map: Map, routers: list):
  queue = collections.deque([map.backbone.cell])
  visited = set()
  visited.add(map.backbone.cell)
  while queue:
    possible_cell = queue.popleft()

    if not is_wall(possible_cell, map) and not is_backbone(possible_cell, map) and not is_wired(possible_cell, map) and not is_void(possible_cell, map) and possible_cell not in routers:
      return possible_cell
    
    for adj in adjacents(possible_cell):
      if 0 <= adj.x < map.rows and 0 <= adj.y < map.columns and adj not in visited:
        visited.add(adj)
        queue.append(adj)
  
  return None """

""" def compute_targets(map: Map, router: Router):
  targets = set()
  range_ = router.range_
  rx, ry = router.cell.x, router.cell.y

  for x in range(max(0, rx - range_), min(map.rows, rx + range_ + 1)):
    for y in range(max(0, ry - range_), min(map.columns, ry + range_ + 1)):
      if abs(rx - x) <= range_ and abs(ry - y) <= range_:
        if not any(is_wall(Cell(w, v), map) for w in range(min(rx, x), max(rx, x)) for v in range(min(ry, y), max(ry, y))):
          possible_target = Cell(x, y)
          
          if is_target(possible_target, map):
            targets.add(possible_target)

  return targets """

""" 
def greedy(map: Map, router_cost, router_range):
  solution = Solution([], 0, set())

  while True:
    # find the closest available cell of the backbone to place a router
    cell_to_router = find_nearest_available_cell_to_router(map, [router.cell for router in solution.routers])

    if(cell_to_router is None):
      break

    # create the router
    router = routerClass.Router(cell_to_router, router_cost, router_range)
    
    # find the shortest path between the router and the backbone
    path = bfs.bfs(map, map.backbone.cell, router.cell)

    # update cost
    new_cost = solution.cost + router_cost + map.backbone.cost * (len(path)-1)

    if new_cost <= map.budget:
      solution.cost = new_cost
      solution.routers.append(router)
      solution.fiber.update(path)

      # update targets based on the new router
      map.wired.update(compute_targets(map, router))

      # update the backbone connections
      map.backbone.connected_to.extend(path)
    else:
      break
   
  return solution
 """

import models.cell as cell
import models.map as mapClass
import models.router as router


def draw_pixel(screen, x, y, color):
    pygame.draw.rect(screen, color, (x, y, 1, 1))

def draw_pixel_resize(screen, x, y, color):
    pygame.draw.rect(screen, color, (x*2, y*2, 2, 2))


def draw_map(screen, m: mapClass.Map):
  void = (0, 0, 0)
  wall = (128, 128, 128)
  target = (255, 255, 0)

  for i in m.walls:
    draw_pixel_resize(screen, i.x, i.y, wall)
  for i in m.voids:
    draw_pixel_resize(screen, i.x, i.y, void)
  for i in m.targets:
    draw_pixel_resize(screen, i.x, i.y, target)
  pygame.display.flip()
  print("Map Drawn")

def main():
  pygame.init()

  out = open("output.txt", "w")

  m : mapClass.Map
  state = 'MENU'
  title_text = 'Hello, choose the file!'
  texts = ['Simple Example', 'Charleston Road', 'Lets Go Higher', 'Opera', 'Rue De Londres']
  file_options = ['example.in', 'charleston_road.in', 'lets_go_higher.in', 'opera.in', 'rue_de_londres.in']
  algorithms = ['Random', 'Greedy', 'Hill Climbing', 'Simulated Annealing', 'Tabu Search', 'Genetic Algorithm']



  void = (0, 0, 0)
  wall = (128, 128, 128)
  target = (255, 255, 0)
  target_router = (0, 255, 0)
  backbone = (255, 0, 0)
  router = (0, 0, 255)


  choice_map = 0

  choice_alg = 0

  font = pygame.font.SysFont(None, 55)

  screen = pygame.display.set_mode((1000, 900))
  pygame.display.set_caption('Router Placement')

  hwnd = pygame.display.get_wm_info()['window']

  # Move the window to the top-left corner
  ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0)


  title = font.render(title_text, True, (255, 255, 255))

  

  running = True
  while running:
    for event in pygame.event.get():
      if state == 'MENU':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
          elif event.key == pygame.K_DOWN:
            choice_map = (choice_map + 1) % len(texts)
          elif event.key == pygame.K_UP:
            choice_map = (choice_map - 1) % len(texts)
          elif event.key == pygame.K_RETURN:
            pygame.display.set_caption('Router Placement - ' + texts[choice_map])
            path = "../maps/"+file_options[choice_map]
            m = utils.parse(path)
            state = 'ALGCHOICE'
      elif state == 'ALGCHOICE':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            state = 'MENU'
          elif event.key == pygame.K_DOWN:
            choice_alg = (choice_alg + 1) % len(algorithms)
          elif event.key == pygame.K_UP:
            choice_alg = (choice_alg - 1) % len(algorithms)
          elif event.key == pygame.K_RETURN:
            pygame.display.set_caption('Router Placement - ' + texts[choice_map] + ' - ' +algorithms[choice_alg])
            screen.fill((0, 0, 0))
            draw_map(screen, m)
            pygame.display.flip()
            state = 'ALGORITHM'
      elif state == 'ALGORITHM':
        if(choice_alg == 0):
          sol = randomSolution.randomSolution(m)
          print(sol)
          print(m.evaluate(sol))
          state = 'ALGCHOICE'

        elif(choice_alg == 1):
          draw_map(screen, m)
          sol = greedySolution.greedySolution(m)
          print(sol)
          print(m.evaluate(sol))
          targets = sol.getTargets()
          routerCells = list(map(lambda router: router.cell,sol.routers))
          print("Screen Blackout")
          screen.fill((0, 0, 0))
          print("Drawing")


          for j in range(0,m.rows):
            for i in range(0,m.columns):
              newCell = cell.Cell(i,j)
              if(newCell in routerCells):
                draw_pixel_resize(screen, i, j, router)
                print("r",end="")
                out.write("r")
              elif newCell in targets:
                draw_pixel_resize(screen, i, j, target_router)
                print("x",end="")
                out.write("x")
              elif m.isWall(newCell):
                draw_pixel_resize(screen, i, j, wall)
                print("w",end="")
                out.write("w")
              elif m.isVoid(newCell):
                draw_pixel_resize(screen, i, j, void)
                print("-",end="")
                out.write("-")
              else:
                draw_pixel_resize(screen, i, j, target)
                print(" ",end="")
                out.write(" ")

            print()
            out.write("\n")
          pygame.display.flip()
          state = 'FROZEN'
          print("Done")
          out.close()


        else:
          state = 'NOT_IMPLEMENTED'
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              running = False
      elif state == 'NOT_IMPLEMENTED':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            state = 'ALGCHOICE'
      elif state == 'FROZEN':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False

    
    # print(solGreedy)
    if state == 'MENU':
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the title on the screen
        screen.blit(title, (10, 50))

        # Draw the options on the screen
        y = 150
        for i, text in enumerate(texts):
            color = (255, 255, 255) if i != choice_map else (255, 0, 0)
            rendered_text = font.render(text, True, color)
            screen.blit(rendered_text, (10, y))
            y += 60  # Adjust the y position for the next text

        # Update the display
        pygame.display.flip()

    elif state == 'ALGCHOICE':
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the title on the screen
        screen.blit(title, (10, 50))

        # Draw the options on the screen
        y = 150
        for i, text in enumerate(algorithms):
            color = (255, 255, 255) if i != choice_alg else (255, 0, 0)
            rendered_text = font.render(text, True, color)
            screen.blit(rendered_text, (10, y))
            y += 60  # Adjust the y position for the next text

        # Update the display
        pygame.display.flip()
    
    elif state == 'NOT_IMPLEMENTED':
      screen.fill((0, 0, 0))
      text = font.render('Not implemented yet', True, (255, 0, 0))
      screen.blit(text, (10, 50))
      pygame.display.flip()


    elif state == 'FROZEN':
      pygame.display.flip()
          
        


  

if __name__ == "__main__":
  main()
