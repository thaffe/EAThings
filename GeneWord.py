from random import randint, random
from Gene import Gene


class GeneWord(Gene):

    def mutate(self, mutation_rate):
        for i in xrange(len(self.letters)):
            if random() < mutation_rate:
                self.letters[i] = randint(0, self.alphabet_size)

    def random_value(self, source):
        self.letters = []
        self.alphabet_size = source.alphabet_size
        self.letters = [randint(0, source.alphabet_size) for _ in xrange(self.alphabet_size)]
