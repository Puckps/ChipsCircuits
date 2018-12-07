# add directories to path
import sys, os
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "results"))
sys.path.append(os.path.join(directory, "code" , "algorithms"))

from classChip import *
from load_data import load_data
from a_star import *
from greedy import *
from genetic import *
import visualization
import argparse

def main():

	"""
		load circuits and netlists
	"""
	circuits = load_data(directory + "/data/circuits.txt")
	netlists = load_data(directory + "/data/netlists.txt")

	"""
		Extract program input
	"""
	# TODO make a function for this

	# add parser for command line arguments
	parser = argparse.ArgumentParser(description="Chips & Circuits. If run without positional arguments deafult program is runned.")

	# add all possible algorithms/circuits/netlists to dicts
	algorithmsdict = {"greedy" : greedy, "a_star" : a_star,
					  "both" : (greedy, a_star)}
	circuitsdict = {"small" : circuits.circuit_0, "large": circuits.circuit_1,
					"both" : (circuits.circuit_0, circuits.circuit_1)}
	netlistsdict = {1 : netlists.netlist_1, 2 : netlists.netlist_2,
					3: netlists.netlist_3, 4 : netlists.netlist_4,
					5: netlists.netlist_5, 6 : netlists.netlist_6,
					"small" : (netlists.netlist_1, netlists.netlist_2,
							 netlists.netlist_3),
					"large" : (netlists.netlist_4, netlists.netlist_5,
							 netlists.netlist_6),
					"all" : (netlists.netlist_1, netlists.netlist_2,
							 netlists.netlist_3, netlists.netlist_4,
							 netlists.netlist_5, netlists.netlist_6)}
	visualization_optionsdict = {"true" : True, "false" : False}

	# dimensions in (width, height)
	chip_dimensionsdict = {"small" : (18, 13), "large" : (18, 17)}

	# add parser arguments
	parser.add_argument("algorithm", choices=algorithmsdict.keys(), nargs="?", default="both", help="Choose algorithm: greedy/a_star/both. Default is both")
	parser.add_argument("circuit", choices=circuitsdict.keys(), nargs="?", default="both", help="Choose circuit: small/large/both. Default is both. Choose small netlist with small circuit and large netlist with large circuit")
	parser.add_argument("netlist", choices=netlistsdict.keys(), nargs="?", default="all", help="Choose circuit: 1/2/3/4/5/6/small/large/all. Default is all. Choose small netlist with small circuit and large netlist with large circuit")
	parser.add_argument("-v", "--visualization", choices=visualization_optionsdict.keys(), default="false", help="Show visualization: true/false. Default is false")
	args = parser.parse_args()
	argsdict = vars(args) 		# dict with all args stored by keys

	# Extract arguments
	algorithmslist = []
	if (argsdict["algorithm"]) == "both":
		algorithmslist = [algorithmsdict[args.algorithm][i] for i in range(len(algorithmsdict[args.algorithm]))]
	else:
		algorithmslist.append(algorithmsdict[args.algorithm])

	# Extract arguments
	circuitslist = []
	L_chips = ["small", "large"]
	if (argsdict["circuit"] == "both"):
		for i in range(len(circuitsdict[args.circuit])):
			circuitslist.append((circuitsdict[args.circuit][i], L_chips[i]))
	elif (argsdict["circuit"] == "small"):
		circuitslist.append((circuitsdict[args.circuit], "small"))
	elif (argsdict["circuit"] == "large"):
		circuitslist.append((circuitsdict[args.circuit], "large"))

	# Extract arguments
	netlistslist = []
	L_netlists = [1, 2, 3, 4, 5, 6]
	if (argsdict["netlist"]) == "all":
		netlistslist = [(netlistsdict[args.netlist][i], L_netlists[i]) for i in range(len(netlistsdict[args.netlist]))]
	elif (argsdict["netlist"]) == "large":
		netlistslist = [(netlistsdict[args.netlist][i], L_netlists[i+3]) for i in range(len(netlistsdict[args.netlist]))]
	elif (argsdict["netlist"]) == "small":
		netlistslist = [(netlistsdict[args.netlist][i], L_netlists[i]) for i in range(len(netlistsdict[args.netlist]))]
	else:
		netlists.append(argsdict[args.netlist])

	do_visualization = False
	if argsdict["visualization"] == "true":
		do_visualization = True

	# circuit = circuits.circuit_1
	# netlist = netlists.netlist_6
	# algorithm = a_star
	# width, height = 18, 17

	"""
		state space size and upper/lower bounds for given chip and netlist
	"""

	for circuit in circuitslist:
		for netlist in netlistslist:
			if (circuit[1] == "small" and (netlist[1] == 1 or netlist[1] == 2 or netlist[1] == 3)) or (circuit[1] == "large" and (netlist[1] == 4 or netlist[1] == 5 or netlist[1] == 6)):
				width, height = chip_dimensionsdict[circuit[1]]
				print("Calculating state space for circuit " + circuit[1] +
					  " and netlist " + str(netlist[1]))
				state_space(circuit[0], width, height, netlist[0])
				print()
			else:
				print("No compatible circuits and netlists selected! Run main.py -h for help")
				exit(1)

	"""
		run desired algorithm
	"""

	for algorithm in algorithmslist:
		for circuit in circuitslist:
			for netlist in netlistslist:
				if (circuit[1] == "small" and (netlist[1] == 1 or netlist[1] == 2 or netlist[1] == 3)) or (circuit[1] == "large" and (netlist[1] == 4 or netlist[1] == 5 or netlist[1] == 6)):
					width, height = chip_dimensionsdict[circuit[1]]
					population_size = 20
					if algorithm == a_star:
						netlist, fitness = make_netlist(population_size, circuit[0], width, height, algorithm, netlist[0])
						total_cost = upper_bound(Chip(circuit, width, height)) - fitness
					else:
						total_cost = test_algorithm(circuit[0], width, height, netlist[0], algorithm, do_visualization)
					# test algorithm with netlist obtained from genetic algorithm
					print("Total cost", algorithm.__name__, " = ", total_cost)
	return

def test_algorithm(circuit, width, height, netlist, algorithm, do_visualization, random_layers=False):
	cost = 0
	while cost == 0:
		chip = Chip(circuit, width, height)
		chip.load_chip()
		for net in netlist:
			try:
				cost += algorithm(chip, net, int(random() * len(netlist) / 10 + 1))
			except KeyError:
				cost = 0
				break

	# print grid
	if do_visualization == True:
		visualization.plot_3D(directory + "/results", chip, width, height)
		visualization.plot_grid(directory + "/results", chip, width, height)

	return cost

if __name__ == "__main__":
	main()
