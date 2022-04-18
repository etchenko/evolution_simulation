import pyglet
import random
from brain import brain

MAX_SPEED = 10

### NOTES
'''
    The genome in simplest terms could control the probability that they move in a given direction
'''

'''
The class for the organisms which will evolve
'''
class organism(pyglet.shapes.Circle):
    def __init__(self, xrange, yrange, batch, genome, radius = 5):
        # Get the color of the organism based on the hash of the genome
        gen_len = int(len(genome)/3)
        color = (hash(genome[:gen_len]) % 256, hash(genome[gen_len:gen_len*2]) % 256, hash(genome[gen_len*2:]) % 256)

        # Call the super constructor
        super(organism, self).__init__(x = random.uniform(xrange[0], xrange[1]),
                                       y = random.uniform(yrange[0], yrange[1]),
                                       radius = radius, 
                                       color = color, 
                                       batch = batch)
        # Initialize the variables
        self.genome = genome
        self.direction = random.randint(0,3)
        speed = 0
        for i in range(12, 16, 1):
            speed += ord(genome[i]) - 65
        self.velocity = (speed/100)* MAX_SPEED
        self.energy = 0
        self.brain = brain(genome[:12])
        self.xrange = xrange
        self.yrange = yrange
    
    '''
    Each time step, update the organism
    '''
    def update(self, dt, state):
        dir = self.brain.think(state)
        if dir == 0:
            self.move(self.velocity,0)
        elif dir == 1:
            self.move(0,self.velocity)
        elif dir == 2:
            self.move(-self.velocity,0)
        elif dir == 3:
            self.move(0,-self.velocity)

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

    '''
    Check if the organism is dead
    '''
    def is_dead(self):
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