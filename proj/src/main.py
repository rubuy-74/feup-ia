import sys
import pygame
import yaml

import time

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import utils
import menu.draw as draw

from algorithms.naive import naive
from algorithms.hillclimb import hillclimb
from algorithms.simulatedAnnealing import simulated_annealing
from algorithms.genetic import genetic

STATE_RUNNING = 'ALGORITHM'
STATE_FROZEN = 'FROZEN'

class RouterPlacementGame:
    def __init__(self, config_path):
        pygame.init()
        
        self.screen = pygame.display.set_mode((1000, 900))
        
        pygame.display.set_caption('Router Placement')
        
        self.config = self.load_config(config_path)
        
        self.state = STATE_RUNNING
        self.stop_algorithm = False
        

    def load_config(self, config_file):
        with open(config_file) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.map = config['map']
            self.algo = config['algorithm']
            self.seed = config['seed']
            self.size = config['size']
            self.probs = config['probabilities']
            self.constraints = config['constraints']
            

    def run(self):
        self.execute_algorithm()
        
        self.state = STATE_FROZEN
        
        while self.state == STATE_FROZEN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            pygame.display.flip()

                
            
    def execute_algorithm(self):
        m = utils.parse("../maps/" + self.map)
        
        self.screen.fill((0, 0, 0))

        if(self.map == 'lets_go_higher.in'):
            m = utils.parse("../output/" + self.map)
        else:
            draw.draw_map(self.screen, m, self.size)
            
        stop_condition = False 
        
        def should_stop():
            nonlocal stop_condition
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    stop_condition = True
                    return True
            return False   
        
        solutions = []
        if self.algo == 'naive':
            start = time.time()
            m, remaining_budget = naive(m, self.constraints['budget'], self.map == 'lets_go_higher.in')
            it = 1
            time_spent = time.time() - start
        elif self.algo == 'hill_climbing':
            m, remaining_budget = naive(m, self.constraints['budget'], self.map == 'lets_go_higher.in')
            
            m, remaining_budget, solutions, it, time_spent = hillclimb(m, remaining_budget, self.probs, stop_condition=should_stop)
            
        elif self.algo == 'simulated_annealing':
            current_map, remaining_budget = naive(m, self.constraints['budget'], self.map == 'lets_go_higher.in')
            
            m, remaining_budget, solutions, it, time_spent = simulated_annealing(current_map, remaining_budget, self.probs, stop_condition=should_stop)
            
        elif self.algo == 'genetic':
            (m, remaining_budget), solutions, it, time_spent = genetic(m, self.probs, self.constraints['budget'],stop_condition=should_stop)

        if m:
            draw.draw_solution(self.screen, m, self.size)
            utils.dump_solution(f"{self.map[:-3]}_{self.algo}.out", m, remaining_budget, it, time_spent)
            if(len(solutions) > 0):
                plt.plot(range(len(solutions)),solutions,marker='o')
                plt.xlabel('Iterations')
                plt.ylabel('Score')

                plt.grid(True)
                plt.savefig(f"../output/v2/{self.map[:-3]}_{self.algo}.png")
            
        self.state = STATE_FROZEN


if __name__ == "__main__":
    config = ''
    if len(sys.argv) > 1:
        config_path = f"../configs/{sys.argv[1]}"
        if os.path.exists(config_path):
            game = RouterPlacementGame(config_path)
            game.run()
        else:
            print(f"Error: Config file '{config_path}' not found.")
            pass
    else:
        print(f"Error: You must pass a config file.")
        pass
    
