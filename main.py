'''
IDEAS:
    Program
        1. Have some sort of way to be able to view the organism details, maybe when the game is paused it shows you
            the details of one of the organisms, and to rotate through them you press forward or back
        3. Add buttons or text boxes where you can specify all of the specific variables (Like number, generation time, 
            length, etc), and then a reset button at the end which will reset the simulation with those specifications
        4. You could also add a brain selection button where you can choose what type of brain the organisms have 
            during a given simulation
    Organisms:
        1. Have a field of vision (either a circle around them, or maybe some sort of cone in front of them) which can
            then be an input into the brain
            b. The field of vision could also just be the closest 3 foods
        2. Have a version of the brain which is a neural network based on the visual field input
        3. Make the organisms be able to be carnivorous
    Environment
        1. Have different aread of the environment (visible in the visual field), where maybe food is more abundant or
            more scarse, or maybe where movement may be slowed down, or they use up more energy being in those
            environments
        2. Have poison foods, where if they eat a specific food type they will get posioned
    
    Other
        1. Instead of vision, give the cell some memory about which environments it was in the last few steps and
            whether or not it found food, or even just its vision is the current environment in which is is in.
    
    
'''

from __future__ import division

from numpy import average
from pyglet.window import key
import pyglet
import matplotlib.pyplot as plt

import sim

GENE_LENGTH = 10
ELITISM = 5
MUTATION_RATE = 2/(GENE_LENGTH)
ORG_RADIUS = 5
FOOD_RADIUS = 2
SPEED = 120
WIDTH = 800
HEIGHT= 800
XRANGE = (100,700)
YRANGE = (100,700)
ORGS = 50
FOOD_COUNT = 500
GRID_WIDTH, GRID_HEIGHT = XRANGE[1] - XRANGE[0], YRANGE[1]-YRANGE[0]
FOOD_PROB = .5
FOOD_TYPE = 0
DIRECTIONS = 3

# Create the game window
game_window = pyglet.window.Window(
    width=WIDTH,
    height=HEIGHT,
    caption="Evolution Simulation"
)

settings = { 'food_prob': FOOD_PROB, 'gene_length': GENE_LENGTH, 'elitism': ELITISM, 'mutation_rate': MUTATION_RATE, 
            'org_radius':ORG_RADIUS, 'food_radius':FOOD_RADIUS, 'xrange':XRANGE, 
            'yrange':YRANGE, 'orgs':ORGS, 'food_count':FOOD_COUNT, 'height':HEIGHT, 'width':WIDTH,'food_type':FOOD_TYPE, 
            'dirs': DIRECTIONS}

'''
What to do each time the game updates
'''
@game_window.event
def on_draw():
    game_window.clear()
    rectangles.draw()
    game.draw()
    fps.draw()
    labels.draw()
    if not running:
        pause.draw()


'''
What to do in the event of a keypress
'''
@game_window.event
def on_key_press(symbol, modifiers):
    global player_x, player_y, SPEED, running
    if symbol == key.LEFT:
        if SPEED > 2:
            SPEED = SPEED / 2
        pyglet.clock.unschedule(update)
        pyglet.clock.schedule_interval(update, 1/SPEED)
        update_labels()
    elif symbol == key.RIGHT:
        if SPEED < 960:
            SPEED = SPEED * 2
        pyglet.clock.unschedule(update)
        pyglet.clock.schedule_interval(update, 1/SPEED)
        update_labels()
    elif symbol == key.UP:
        game.reset()
        update_labels()
    elif symbol == key.DOWN:
        GENERATION_LENGTH -= 100
        update_labels()
    elif symbol == key.SPACE:
        if running:
            pyglet.clock.unschedule(update)
            running = False
        else:
            pyglet.clock.schedule_interval(update, 1/SPEED)
            running = True
    elif symbol == key._1:
        settings['food_type'] = 0
        settings['mutation_rate'] = 10/((GENE_LENGTH))
        settings['food_count'] = 500
        settings['food_prob'] = .5
        settings['orgs'] = 50
        game.reset()
    elif symbol == key._2:
        settings['food_type'] = 1
        settings['food_prob'] = .5
        settings['food_count'] = 500
        settings['mutation_rate'] = 2/(GENE_LENGTH)
        game.reset()
    elif symbol == key._3:
        settings['food_type'] = 2
        settings['mutation_rate'] = 2/(GENE_LENGTH)
        game.reset()
    elif symbol == key._4:
        settings['food_type'] = 3
        settings['mutation_rate'] = 2/(GENE_LENGTH)
        game.reset()
    elif symbol == key.P:
        count = game.count
        plot1 = plt.plot(count, label = 'Organism count')
        plt.title('Simulation Organism Count')
        plt.xlabel('Time (timesteps)')
        plt.ylabel('Organisms')
        plt.legend()
        plt.yticks([])
        plt.show(block=True)
    elif symbol == key.T:
        count = game.count
        plot1 = plt.plot(count, label ='Organism count')
        foods = game.food_count
        org_av = average(count)
        fo_av = average(foods)
        scaling = fo_av/org_av
        foods = [i/scaling for i in foods]
        plot2 = plt.plot(foods, label = 'Food count')
        plt.title('Simulation Organism and Food Count')
        plt.xlabel('Time (timestamp)')
        plt.ylabel('Organisms and Food Count')
        plt.legend()
        plt.yticks([])
        plt.show(block=True)



'''
Update the labels shown in the game
'''
def update_labels():
    global fps, GENERATION_LENGTH
    fps = pyglet.text.Label(f'Speed: {SPEED}',
                          font_name='Times New Roman',
                          font_size=12,
                          x=30, y=15,
                          color=(0,0,0,125))

'''
Update the game at each time tick
'''
def update(dt):
    game.update(dt)

labels = pyglet.graphics.Batch()



fps = pyglet.text.Label(f'Speed: {SPEED}',
                          font_name='Times New Roman',
                          font_size=12,
                          x=30, y=15,
                          color=(0,0,0,125))

# Make the mouse invisible and make the screen white
game_window.set_mouse_visible(False)
pyglet.gl.glClearColor(1, 1, 1, 1)
    
game = sim.simulation(settings)
running = True
pause = pyglet.text.Label('PAUSED',
                          font_name='Times New Roman',
                          font_size=128,
                          x=WIDTH/2, y=HEIGHT/2,
                          anchor_x='center', anchor_y='center',
                          color=(0,0,0,200))
rectangles = pyglet.graphics.Batch()
rect2 = pyglet.shapes.Rectangle(x = WIDTH/2 - GRID_WIDTH/2 - 10,
                                       y = HEIGHT/2 - GRID_HEIGHT/2 - 10,
                                       width = GRID_WIDTH + 20,
                                       height = GRID_HEIGHT + 20, 
                                       color = (0,0,0),
                                       batch = rectangles)
rect1 = pyglet.shapes.Rectangle(x = WIDTH/2 -GRID_WIDTH/2,
                                       y = HEIGHT/2 - GRID_HEIGHT/2,
                                       width = GRID_WIDTH,
                                       height = GRID_HEIGHT, 
                                       color = (255,255,255),
                                       batch = rectangles)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/SPEED)
    pyglet.app.run()