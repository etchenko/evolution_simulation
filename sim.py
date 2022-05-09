import pyglet
import random
import string
from datetime import datetime

from items import organism, food

FOOD_ENERGY = 100
BIRTH_COST = 75
START_ENERGY = 50
food_type = 1
TYPE_2 = 200
TYPE_3 = 100
FOOD_SPARSE = .1


class simulation:
    def __init__(self, settings):
        # Create array of food and organisms
        self.settings = settings
        self.organisms = pyglet.graphics.Batch()
        self.orgs = []
        self.foods = pyglet.graphics.Batch()
        self.f_array = []
        # Add organisms to the simulation
        self.reset()

    '''
    Reset the simulation
    '''
    def reset(self):
        self.orgs = []
        self.f_array = []
        for i in range(self.settings['orgs']):
            genes = ''.join(random.choices(string.ascii_uppercase, k = self.settings['gene_length']))
            org_settings = {
                'start': (self.settings['xrange'][0], self.settings['xrange'][1], 
                        self.settings['yrange'][0], self.settings['yrange'][1]),
                'xrange': self.settings['xrange'], 'yrange': self.settings['yrange'],
                'batch': self.organisms, 'genome': genes, 'energy': START_ENERGY
            }
            self.orgs.append(organism(org_settings))
        for i in range(self.settings['food_count']):
            self.generate_food(food_type)

    '''
    Draw the simulation
    '''
    def draw(self):
        self.organisms.draw()
        self.foods.draw()

    '''
    Update the simulation state at every time step
    '''
    def update(self, dt):
        '''
        state = [[0 for i in range(self.HEIGHT - 300)] for j in range(self.WIDTH - 200)]
        for fo in self.f_array:
            x = round(fo.x)
            y = round(fo.y)
            state[y][x] = 1
        for org in self.orgs:
            x = round(org.x)
            y = org.y
            #state[y][x] = 2
        '''

        # Update the position of the organisms
        for org in self.orgs:
            org.update(dt)
        
        # Have the organisms eat the food
        count = 0
        for f in self.f_array:
            for org in self.orgs:
                if f.x - 4 < org.x < f.x + 4 and  f.y - 4 < org.y < f.y + 4:
                    org.energy += f.energy
                    self.f_array.remove(f)
                    del(f)
                    count+= 1
                    break
        for i in range(count):
            self.generate_food(food_type)
        
        # Check if dead or pregnant
        for i, org in enumerate(self.orgs):
            if org.is_pregnant():
                org_settings = {
                'start': (org.x - 5, org.x + 5, org.y - 5, org.y + 5),
                'xrange': self.settings['xrange'], 'yrange': self.settings['yrange'],
                'batch': self.organisms, 'genome': self.mutate(org.genome), 'energy': org.energy/2
            }
                self.orgs.append(organism(org_settings))
                org.energy -= org.energy/2
            if org.is_dead():
                del(self.orgs[i])

    '''
    Mutate a genome randomly
    '''
    def mutate(self, genome):
        new = ''
        for i in genome:
            rand = random.random()
            if rand < self.settings['mutation_rate']:
                i = random.choice(string.ascii_uppercase)
            new += i
        return new

    def generate_food(self, food_type):
        # Totally random food generation
        if food_type == 0:
            self.f_array.append(food(self.settings['xrange'],self.settings['yrange'], self.foods, 
                        energy = FOOD_ENERGY))
        # Food more present in the center of the box
        if food_type == 1:
            rand = random.random()
            if rand < FOOD_SPARSE:
                self.f_array.append(food(self.settings['xrange'],self.settings['yrange'], self.foods, 
                            energy = FOOD_ENERGY))
            else:
                self.f_array.append(food((self.settings['xrange'][0] + TYPE_2, self.settings['xrange'][1] - TYPE_2),
                            (self.settings['yrange'][0] + TYPE_2, self.settings['yrange'][1] - TYPE_2), self.foods,
                            energy = FOOD_ENERGY))
        
        # Food more present in the corners
        if food_type == 2:
            rand = random.random()
            if rand < FOOD_SPARSE:
                self.f_array.append(food(self.settings['xrange'],self.settings['yrange'], self.foods, 
                            energy = FOOD_ENERGY))
            elif rand < FOOD_SPARSE + (1-FOOD_SPARSE)/4:
                # Bottom Right
                self.f_array.append(food((self.settings['xrange'][0] + TYPE_2, self.settings['xrange'][1] - TYPE_2),
                            (self.settings['yrange'][0] + TYPE_2, self.settings['yrange'][1] - TYPE_2), self.foods,
                            energy = FOOD_ENERGY))
            elif rand < FOOD_SPARSE + (1-FOOD_SPARSE)/2:
                # Bottom Left
            elif rand < FOOD_SPARSE + (1-FOOD_SPARSE)/4*3:
                #Top Right
            else:
                # Top left
