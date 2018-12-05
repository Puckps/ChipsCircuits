# put all functions that is used by multiple algorithms
from classChip import *

def distance(coords_a, coords_b):
	return abs(coords_a[0] - coords_b[0]) + abs(coords_a[1] - coords_b[1])
	
def heuristic(coords_a, coords_b):
	return abs(coords_a[0] - coords_b[0]) + abs(coords_a[1] - coords_b[1]) + abs(coords_a[2] - coords_b[2])

def gate_density(chip, coordinates):
	dist = 0
	for gate in chip.gates:
		if heuristic(gate.coordinates, coordinates) < 4:
			dist += 1
	return dist

# delta x * delta y, POSSIBLY an improvement; does the simplest/most straight paths first
def area(coords_a, coords_b):
	return abs(coords_a[0] - coords_b[0]) * abs(coords_a[1] - coords_b[1])

# largest lower bound
def lower_bound(circuit, netlist):
	lower_bound = 0
	for net in netlist:
		lower_bound += distance(circuit[net[0]], circuit[net[1]])
	return lower_bound

# smallest upper bound
def upper_bound(chip):
	return chip.width * chip.height * chip.max_levels