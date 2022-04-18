import pyglet
import random
import string
from datetime import datetime

from items import organism, food

class simulation:
    def __init__(self, p, GENE_LENGTH, ELITISM, MUTATION_RATE, GENERATION_LENGTH, ORG_RADIUS, FOOD_RADIUS, XRANGE, YRANGE, ORGS, FOOD_COUNT, HEIGHT, WIDTH):
        # Create array of food and organisms
        self.GENE_LENGTH, self.ELITISM, self.MUTATION_RATE = GENE_LENGTH, ELITISM, MUTATION_RATE
        self.GENERATION_LENGTH, self.ORG_RADIUS, self.FOOD_RADIUS = GENERATION_LENGTH, ORG_RADIUS, FOOD_RADIUS
        self.XRANGE, self.YRANGE, self.HEIGHT, self.WIDTH = XRANGE, YRANGE, HEIGHT, WIDTH
        self.ORGS, self.FOOD_COUNT = ORGS, FOOD_COUNT
        self.organisms = pyglet.graphics.Batch()
        self.orgs = []
        self.foods = pyglet.graphics.Batch()
        self.f_array = []
        # Add organisms to the simulation
        for i in range(self.ORGS):
            genes = ''.join(random.choices(string.ascii_uppercase, k = self.GENE_LENGTH))
            self.orgs.append(organism(xrange = self.XRANGE, yrange = self.YRANGE, batch = self.organisms, genome = genes))
        
        for i in range(self.FOOD_COUNT):
            self.f_array.append(food(self.XRANGE,self.YRANGE, self.foods, energy = 1))
        
        self.food_prob = p
        self.count = 0
        self.generation = 1
        self.start = datetime.now()
        self.change_stats()
    
    '''
    Draw the simulation
    '''
    def draw(self):
        self.organisms.draw()
        self.foods.draw()
        self.label.draw()
        self.time.draw()


    '''
    Update the simulation state at every time step
    '''
    def update(self, dt):
        #state = [[0 for i in range(self.HEIGHT - 300)] for j in range(self.WIDTH - 200)]
        for fo in self.f_array:
            x = round(fo.x)
            y = round(fo.y)
            #state[y][x] = 1
        for org in self.orgs:
            x = round(org.x)
            y = org.y
            #state[y][x] = 2

        # Update the position of the organisms
        for organism in self.orgs:
            organism.update(dt, dt)
        
        # Have the organisms eat the food
        for f in self.f_array:
            for org in self.orgs:
                if f.x - 4 < org.x < f.x + 4 and  f.y - 4 < org.y < f.y + 4:
                    org.energy += f.energy
                    self.f_array.remove(f)
                    del(f)
                    break
        
        # Generate new food
        rand = random.random()
        if rand < self.food_prob:
            self.f_array.append(food(self.XRANGE,self.YRANGE, self.foods, energy = 1))
        self.count += 1
        if self.count > self.GENERATION_LENGTH:
            self.count = 0
            self.next_gen()
    '''
    Move to the next generation
    '''
    def next_gen(self):
        self.orgs.sort(key=lambda x: x.energy, reverse=True)
        new = []
        for i in range(self.ELITISM):
            new.append(organism(xrange = self.XRANGE, yrange = self.YRANGE, batch = self.organisms, genome = self.orgs[i].genome))
            for j in range(int(self.ORGS/self.ELITISM)):
                new.append(organism(xrange = self.XRANGE, yrange = self.YRANGE, batch = self.organisms, genome = self.mutate(self.orgs[i].genome)))
        del(self.orgs)
        self.orgs = new
        del(self.f_array)
        self.f_array = []
        for i in range(self.FOOD_COUNT):
            self.f_array.append(food(self.XRANGE,self.YRANGE, self.foods, energy = 1))
        self.generation += 1
        self.change_stats()

    '''
    Mutate a genome randomly
    '''
    def mutate(self, genome):
        new = ''
        for i in genome:
            rand = random.random()
            if rand < self.MUTATION_RATE:
                i = random.choice(string.ascii_uppercase)
            new += i
        return new
    
    '''
    Def: Update the stats that are presented on the screen
    '''
    def change_stats(self):
        self.label = pyglet.text.Label(f'Gen: {self.generation}',
                          font_name='Times New Roman',
                          font_size=36,
                          x=30, y=45,
                          #anchor_x='center', anchor_y='center',
                          color=(0,0,0,125))
        self.time = pyglet.text.Label(f'Generation Time: {datetime.now()- self.start}',
                          font_name='Times New Roman',
                          font_size=12,
                          x=30, y=30,
                          #anchor_x='center', anchor_y='center',
                          color=(0,0,0,125))
        self.start = datetime.now()
