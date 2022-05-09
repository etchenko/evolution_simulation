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
from pyglet.window import key
import pyglet

import sim

GENE_LENGTH = 5
ELITISM = 5
MUTATION_RATE = 1/(GENE_LENGTH)
GENERATION_LENGTH = 800
ORG_RADIUS = 5
FOOD_RADIUS = 2
SPEED = 120
WIDTH = 800
HEIGHT= 800
XRANGE = (100,700)
YRANGE = (100,700)
ORGS = 30
FOOD_COUNT = 500
GRID_WIDTH, GRID_HEIGHT = XRANGE[1] - XRANGE[0], YRANGE[1]-YRANGE[0]
FOOD_PROB = 1

# Create the game window
game_window = pyglet.window.Window(
    width=WIDTH,
    height=HEIGHT,
    caption="Evolution Simulation"
)

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
    global player_x, player_y, SPEED, running, GENERATION_LENGTH
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
    generation_length = pyglet.text.Label(f'Gen Length: {GENERATION_LENGTH}',
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

settings = { 'food_prob': FOOD_PROB, 'gene_length': GENE_LENGTH, 'elitism': ELITISM, 'mutation_rate': MUTATION_RATE, 
            'org_radius':ORG_RADIUS, 'food_radius':FOOD_RADIUS, 'xrange':XRANGE, 
            'yrange':YRANGE, 'orgs':ORGS, 'food_count':FOOD_COUNT, 'height':HEIGHT, 'width':WIDTH }
    
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