import random

class brain:
    def __init__(self, genome):
        self.genome = genome
        chars = []
        for char in genome:
            chars.append(ord(char) - 65)

        # Create the first instantiation of a 'brain'
        self.probs = [chars[i] + chars[i + 1] + chars[i + 2] for i in range(0, len(chars) - 1, 3)]
        s = sum(self.probs)
        self.probs = [i/s for i in self.probs]
        for i in range(1,4,1):
            self.probs[i] = self.probs[i] + self.probs[i-1]

    def think(self, state):
        rand = random.random()
        for i, prob in enumerate(self.probs):
            if rand < prob:
                return i
        return 3