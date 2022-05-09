import pyglet
import random
from brain import brain

MAX_SPEED = 10
BIRTH_ENERGY = 1000
MOVE_ENERGY = 2
BIRTH_TIME = 100

'''
The class for the organisms which will evolve
'''
class organism(pyglet.shapes.Circle):
    def __init__(self, settings, radius = 5):
        self.genome = settings['genome']
        # Get the color of the organism based on the hash of the genome
        gen_len = int(len(self.genome)/3)
        color = (hash(self.genome[:gen_len]) % 256, hash(self.genome[gen_len:gen_len*2]) % 256, hash(self.genome[gen_len*2:]) % 256)

        # Call the super constructor
        super(organism, self).__init__(x = random.uniform(settings['start'][0], settings['start'][1]),
                                       y = random.uniform(settings['start'][2], settings['start'][3]),
                                       radius = radius, 
                                       color = color, 
                                       batch = settings['batch'])
        # Initialize the variables
        self.direction = random.randint(0,3)
        speed = 0
        speed += ord(self.genome[4]) - 65
        self.velocity = (speed/100)* MAX_SPEED
        self.energy = settings['energy']
        self.brain = brain(self.genome[:12])
        self.xrange = settings['xrange']
        self.yrange = settings['yrange']
        self.birth_timer = 0
    
    '''
    Each time step, update the organism
    '''
    def update(self, state):
        dir = self.brain.think(state)
        if dir == 0:
            self.move(self.velocity,0)
        elif dir == 1:
            self.move(0,self.velocity)
        elif dir == 2:
            self.move(-self.velocity,0)
        elif dir == 3:
            self.move(0,-self.velocity)
        self.birth_timer += 1

    '''
    Moves the organism in the desrived direction
    '''
    def move(self, x_change, y_change):
        self.x += x_change
        self.y += y_change

        # MAKE SURE THE ORGANISMS STAY IN THE CONFINES OF THE PLANE
        if self.x < self.xrange[0]:
            self.x += self.xrange[1] - self.xrange[0]
        if self.x > self.xrange[1]:
            self.x -= self.xrange[1] - self.xrange[0]
        if self.y < self.yrange[0]:
            self.y += self.yrange[1] -self.yrange[0]
        if self.y > self.yrange[1]:
            self.y -= self.yrange[1] - self.yrange[0]
        self.energy -= MOVE_ENERGY

    '''
    Check if the organism is dead
    '''
    def is_dead(self):
        if self.energy <= 0:
            return True
        return False
    
    def is_pregnant(self):
        if self.energy >= BIRTH_ENERGY and self.birth_timer > BIRTH_TIME:
            self.birth_timer = 0
            return True
        return False

'''
The class for the food
'''
class food(pyglet.shapes.Circle):
    def __init__(self, xrange, yrange, batch, energy, radius = 3):
        super(food, self).__init__(x = random.uniform(xrange[0], xrange[1]),
                                       y = random.uniform(yrange[0], yrange[1]), 
                                       radius = radius, 
                                       color = (50,50,50), 
                                       batch = batch)
        self.energy = energy