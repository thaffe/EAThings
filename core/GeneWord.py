from random import randint, random

from core import Gene


class GeneWord(Gene):

    def mutate(self, mutation_rate):
        for i in xrange(len(self.letters)):
            if random() < mutation_rate:
                self.letters[i] = randint(0, self.alphabet_size)

    def compare(self, other):
        diff = 0
        for i in xrange(len(self.letters)):
            if self.letters[i] != other.letters[i]:
                diff += 1
        diff /= len(self.letters)
        return diff

    def random_value(self, source):
        self.letters = []
        self.alphabet_size = source.alphabet_size
        self.letters = [randint(0, source.alphabet_size) for _ in xrange(self.alphabet_size)]
