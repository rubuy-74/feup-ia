import sys
import pygame
import time
import yaml

import numpy as np
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt

from algorithms.genetic import genetic, crossover
import utils
import menu.draw as draw
import menu.ui as ui
from algorithms.naive import naive
from algorithms.hillclimb import hillclimb
from algorithms.simulatedAnnealing import simulated_annealing
from models.cell import Cell
import copy
from algorithms.functions import mutation_func

# Game States
STATE_MENU = 'MENU'
STATE_ALG_CHOICE = 'ALGCHOICE'
STATE_ALGORITHM = 'ALGORITHM'
STATE_NOT_IMPLEMENTED = 'NOT_IMPLEMENTED'
STATE_FROZEN = 'FROZEN'

class RouterPlacementGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 900))
        pygame.display.set_caption('Router Placement')

        # Game configuration
        self.config = self.load_config('../configs/default.yaml')
        self.config['seed'] = int(time.time() * 1e9)

        # State variables
        self.state = STATE_MENU
        self.choice_map = 0
        self.choice_alg = 0
        self.font = pygame.font.SysFont(None, 55)

        # Define options
        self.texts = ['Charleston Road', 'Lets Go Higher', 'Opera', 'Rue De Londres']
        self.file_options = ['charleston_road.in', 'lets_go_higher.in', 'opera.in', 'rue_de_londres.in']
        self.algorithms = ['Naive', 'Hill Climbing', 'Simulated Annealing' , 'Genetic Algorithm']
        self.algorithms_config = ['naive', 'hillclimbing', 'simulated_annealing', 'genetic_algorithm']

        # Load config if argument is provided
        if len(sys.argv) > 1:
            self.config = self.load_config(f"../configs/{sys.argv[1]}")
            self.state = STATE_ALGORITHM

    def load_config(self, config_file):
        with open(config_file) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                self.handle_event(event)

            ui.display(self.screen, self.state, self.font.render('Choose Config', True, (255, 255, 255)), 
                       self.font, self.texts, self.choice_map, self.algorithms, self.choice_alg)

    def handle_event(self, event):
        if self.state == STATE_MENU:
            self.handle_menu_event(event)
        elif self.state == STATE_ALG_CHOICE:
            self.handle_algorithm_choice_event(event)
        elif self.state == STATE_ALGORITHM:
            self.execute_algorithm()
        elif self.state == STATE_NOT_IMPLEMENTED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = STATE_ALG_CHOICE

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.choice_map = (self.choice_map + 1) % len(self.texts)
            elif event.key == pygame.K_UP:
                self.choice_map = (self.choice_map - 1) % len(self.texts)
            elif event.key == pygame.K_RETURN:
                pygame.display.set_caption(f'Router Placement - {self.texts[self.choice_map]}')
                self.config['size'] = 30 if self.choice_map == 0 else 2 if self.choice_map == 1 else 1
                self.config['map'] = f"{self.file_options[self.choice_map]}"
                self.state = STATE_ALG_CHOICE

    def handle_algorithm_choice_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.choice_alg = (self.choice_alg + 1) % len(self.algorithms)
            elif event.key == pygame.K_UP:
                self.choice_alg = (self.choice_alg - 1) % len(self.algorithms)
            elif event.key == pygame.K_RETURN:
                self.config['algorithm'] = self.algorithms_config[self.choice_alg]
                pygame.display.set_caption(f'Router Placement - {self.texts[self.choice_map]} - {self.algorithms[self.choice_alg]}')
                self.screen.fill((0, 0, 0))
                pygame.display.flip()
                self.state = STATE_ALGORITHM

    def execute_algorithm(self):
        m = utils.parse("../maps/" + self.config['map'])
        self.screen.fill((0, 0, 0))
        values = [] 
        remaining_budget = 0

        if(self.config['map'] == 'lets_go_higher.in'):
            m = utils.parse("../output/" + self.config['map'])
        else:
            draw.draw_map(self.screen, m, self.config['size'])
            
        stop_condition = False 
        
        def should_stop():
            nonlocal stop_condition
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    stop_condition = True
                    return True
            return False   
        
        if self.config['algorithm'] == 'naive':
            solutions = []
            start = time.time()
            m, remaining_budget = naive(m)
            it = 1
            time_spent = time.time() - start
        elif self.config['algorithm'] == 'hillclimbing':
            m, remaining_budget = naive(m, self.config['map'] == 'lets_go_higher.in')
            m, remaining_budget, solutions,it,time_spent= hillclimb(m, remaining_budget, stop_condition=should_stop)
            values = solutions
        elif self.config['algorithm'] == 'simulated_annealing':
            current_map, remaining_budget = naive(m,self.config['map'] == 'lets_go_higher.in')
            m, _, solutions,it,time_spent = simulated_annealing(current_map,remaining_budget=remaining_budget, stop_condition=should_stop)
            values = list(map(lambda x: x.evaluate(0),solutions))
        elif self.config['algorithm'] == 'genetic_algorithm':
            # m, _, solutions = genetic_solution(m)
            (m, remaining_budget),values,it,time_spent = genetic(m, stop_condition=should_stop)
        else:
            self.state = STATE_NOT_IMPLEMENTED
            return

        if m:
            draw.draw_solution(self.screen, m, self.config['size'])
            utils.dump_solution(f"{self.config['map'][:-3]}_{self.config['algorithm']}.out",m,remaining_budget,it,time_spent)
            if(len(solutions) > 0):
                plt.plot(range(len(values)),values,marker='o')
                plt.xlabel('Value')
                plt.ylabel('Index')

                plt.grid(True)
                plt.savefig(f"../output/graphs/{self.config['map'][:-3]}_{self.config['algorithm']}.png")
            
        self.state = STATE_FROZEN


if __name__ == "__main__":
    game = RouterPlacementGame()
    game.run()
