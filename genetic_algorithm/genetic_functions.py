from .individual import Individual
from .nnet import Neural_Network
import numpy as np
import random

def elitist_selection(population, n):
    individuals = sorted(population, key=lambda individual: individual.fitness, reverse=True)
    return individuals[:n]

def roulette_wheel_selection(population, n):
    fitness = [individual.fitness for individual in population]
    fitness_sum = sum(fitness)
    fitness = [f / fitness_sum for f in fitness]

    selected = np.random.choice(population, n, p=fitness)
    return selected

def crossover(mom, dad):
    mom_params, dad_params = mom.nnet.params, dad.nnet.params
    son_params, daughter_params = [], []

    for mom_params_portion, dad_params_portion in zip(mom_params, dad_params):
        option = np.random.choice(["single_point", "SBX"])
        son_params_portion, daughter_params_portion = single_point_crossover(mom_params_portion, dad_params_portion) if option == "single_point" else simulated_binary_crossover(mom_params_portion, dad_params_portion)
        son_params.append(son_params_portion)
        daughter_params.append(daughter_params_portion)

    return (
        Individual(Neural_Network(layer_dims=[32, 20, 12, 4], params=son_params)),
        Individual(Neural_Network(layer_dims=[32, 20, 12, 4], params=daughter_params)))

def simulated_binary_crossover(mom, dad):
    eta = 100
    rand = np.random.uniform(0, 1, mom.shape)
    gamma = np.empty(mom.shape)

    gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (eta + 1))
    gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (eta + 1))

    son = 0.5 * ((1 + gamma) * mom + (1 - gamma) * dad)
    daughter = 0.5 * ((1 - gamma) * mom + (1 + gamma) * dad)

    return son, daughter

def single_point_crossover(mom, dad):
    son = mom.copy()
    daughter = dad.copy()

    rows, cols = mom.shape
    row = np.random.randint(0, rows)
    col = np.random.randint(0, cols)

    son[:row, :] = dad[:row, :]
    daughter[:row, :] = mom[:row, :]

    son[row, :col+1] = dad[row, :col+1]
    daughter[row, :col+1] = mom[row, :col+1]

    return son, daughter

def mutate(individual):
    for params in individual.nnet.params:
        gaussian_mutation(params)

def gaussian_mutation(params):
    scale = .2
    mutation_rate = 0.05

    mutation_array = np.random.uniform(0, 1, size=params.shape) < mutation_rate
    gaussian_mutation = np.random.normal(size=params.shape)

    gaussian_mutation[mutation_array] *= scale

    params[mutation_array] += gaussian_mutation[mutation_array]