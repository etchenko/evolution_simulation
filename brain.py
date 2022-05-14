import random

'''
Neural net brain whose input is the position on the board
'''

class brain:
    def __init__(self, genome, directions):
        self.genome = genome
        chars = []
        for char in genome:
            chars.append(ord(char) - 65)

        # Create the first instantiation of a 'brain'
        self.probs = [chars[i] for i in range(len(chars) - 1)]
        s = sum(self.probs)
        self.probs = [i/s for i in self.probs]
        for i in range(1,directions,1):
            self.probs[i] = self.probs[i] + self.probs[i-1]

    def think(self, state):
        rand = random.random()
        for i, prob in enumerate(self.probs):
            if rand < prob:
                return i
        return 8