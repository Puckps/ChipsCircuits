# Work in progress!

from random import *
from shared_functions import *
from classChip import *

def fitness(chip, netlist, algorithm):
	cost = 0
	for index, net in enumerate(netlist):
		try:
			cost += algorithm(chip, net, int(random() * 8))
		except KeyError:
			return(index)
	return upper_bound(chip) - cost

def initial_pop(size, circuit, width, height, algorithm, netlist):
	population = []
	for i in range(size):
		chip = Chip(circuit, width, height)
		chip.load_chip()
		shuffle(netlist)
		population.append((netlist[:], fitness(chip, netlist[:], algorithm)))
	population.sort(key = lambda netlist : netlist[1], reverse = True)
	return population

def selection(population, sample):
	parents = []
	for i in range(sample):
		parents.append(population[i][0])
	shuffle(parents)
	return parents

def create_child(parent_a, parent_b, netlist):
	temp_netlist = [netlist[i] for i in range(len(netlist))]
	child = [0 for i in range(len(parent_a))]
	for i in range(len(parent_a)):
		if (parent_a[i] == parent_b[i]):
			child[i] = parent_a[i]
			temp_netlist.remove(parent_a[i])
	for i in range(len(child)):
		if (len(netlist) > 0):
			if child[i] == 0:
				child[i] = choice(temp_netlist)
				temp_netlist.remove(child[i])
	return child

def next_pop(population_size, circuit, width, height, algorithm, parents, netlist):
	population = []
	for i in range(len(parents) // 2):
		for j in range(population_size):
			chip = Chip(circuit, width, height)
			chip.load_chip()
			child = create_child(parents[i], parents[len(parents) - 1 - i], netlist)
			population.append((child, fitness(chip, child, algorithm)))
	population.sort(key = lambda child : child[1], reverse = True)
	return population

def mutate(individual):
	ids = range(len(individual))
	a, b = sample(ids, 2)
	individual[a], individual[b] = individual[b], individual[a]

def mutate_pop(population, mutation_rate):
	for individual in population:
		if random() < mutation_rate:
			mutate(individual[0])

def make_netlist(population_size, circuit, width, height, algorithm, netlist):
	population = initial_pop(population_size, circuit, width, height, algorithm, netlist)
	while population[0][1] < len(netlist):
		parents = selection(population, 5)
		population = next_pop(population_size // 5 + 1, circuit, width, height, algorithm, parents, netlist)
		mutate_pop(population, 0.1)
	return population[0][0], population[0][1]