from operator import attrgetter
import math

from core.EA import *


GENERATION_REPLACEMENT = 0
GENERATION_MIXING = 1

#Individual ExpVal = Fitness
def fitness(ea, individuals):
    exp_sum = 0
    for i in individuals:
        i.exp_val = i.fitness
        exp_sum += i.exp_val
    return exp_sum

#Individual ExpVal = 1+(fittnes-mean)/2*SD
def sigma(ea, individuals):
    exp_sum = 0
    for i in individuals:
        i.exp_val = max(0.001, 1 + (i.fitness - ea.mean) / (2 * max(ea.sd, 0.000001)))
        exp_sum += i.exp_val
    return exp_sum


#Retuns random list of individuals
def uniform(ea, individuals):
    shuffle(individuals)
    return individuals[:ea.parent_pool_size]


#Temp = (Max Generations - Current Generation + 1) / Max Generations * Fittnessgoal
def boltz(ea, individuals):
    exp_sum = 0
    temp = ((ea.max_generations - ea.current_generation + 1.0) / ea.max_generations) * ea.fitness_goal
    for i in individuals:
        i.exp_val = math.exp(i.fitness / temp)
        exp_sum += i.exp_val

    avg_exp = exp_sum / len(individuals)
    exp_sum = 0
    for i in individuals:
        i.exp_val /= avg_exp
        exp_sum += i.exp_val
    return exp_sum


rank_max = 1.5
rank_min = 0.5


def rank(ea, individuals):
    exp_sum = 0
    rank = len(individuals)
    rank_delta = rank_max - rank_min
    for i in individuals:
        rank -= 1
        i.exp_val = rank_min + rank_delta * rank / (len(individuals) - 1)
        exp_sum += i.exp_val
    return exp_sum


tournament_k = 5
tournament_e = 0.1


def tournament(ea, individuals):
    tour_index = 0
    l = len(individuals)
    k = tournament_k
    parents = []
    shuffle(individuals)
    while len(parents) < ea.parent_pool_size:
        contenders = individuals[tour_index:max(tour_index + k, l)]

        parents.append(
            max(contenders, key=attrgetter("fitness"))
            if random() > tournament_e else
            contenders[randint(0, tournament_k - 1)]
        )

        tour_index += k
        if tour_index >= l:
            tour_index = 0
            shuffle(individuals)

    return parents


