# Evolution Simulation
![An image of the simulator screen](https://github.com/etchenko/evolution_simulation/simulation.png)
This is an evolution simulator creating as a final project for the Computational Biology course at AIT Budapest during Spring 2022.
# Installation
The only requirements to run this project is to have Python 3.9 on your machine, as well as the matplotlib and pyglet dependencies, which can be installed using pip
```
pip install pyglet
pip install matplotlib
```
# Usage
In order to run the simulation, navigate to the main folder and run the following command:
```
python main.py
```

This will create a pyglet window, and the simulation will begin running there.

## Commands

The program accepts the following keyboard commands:
- SPACEBAR: This will pause the simulation if running, and start the simulation if paused.
- LEFT_ARROW: Slows the speed of the simulation down, as seen in the bottom left corner of the screen
- RIGHT_ARROW: Speeds the simulation up to a maximum of 960 steps per second, as seen in the bottome left corner of the screen
- UP_ARROW: Restarts the simulatin with the current parameters
- P_KEY: Plots a graph of the counts of the organisms up until this point in the simulation
- T_KEY: Plots a graph of the counts of both the organisms and the food up until this point in the simulation
- 1_KEY: Restarts the simulation while setting the food generation to be equally distributed
- 2_KEY: Restarts the simulation while setting the food generation to occur more frequently in the middle of the environment
- 3_KEY: Restarts the simulation while setting the food generation to occur more frequently in the corners of the environment
- 4_KEY: Restarts the simulation while setting the food generatino to occur in lines along the environment  
