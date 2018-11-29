# TODO implement a better visualization
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from termcolor import colored


# print the circuit as a simple grid consisting of seperated layers
def print_simple_grid(chip):
    for z in range(chip.levels):
        print("Layer", z)
        for y in range(chip.height):
            for x in range(chip.width):
                print("|",end="")
                id = str(x) + ", " + str(y) + ", " + str(z)
                if chip.nodes.get(id) is None:
                    print(" ",end="")
                elif chip.nodes.get(id).is_free:
                    print(" ",end="")
                elif chip.nodes.get(id).is_gate:
                    print(colored("o", "red"),end="")
                else:
                    print("-",end="")
            print("|")

# grid representation with matplotlib
def plot_grid(results_directory, chip, width, height):

	# get all gates
	x_gates, y_gates = chip.get_gates_coordinates()
	all_paths_coordinates = chip.get_all_paths_coordinates()

	for level in range(chip.levels):
		if level == 0:
			plot_grid_level(results_directory, width, height,
							all_paths_coordinates=all_paths_coordinates,
							x_gates=x_gates, y_gates=y_gates)
		else:
			plot_grid_level(results_directory, width, height,
							all_paths_coordinates=all_paths_coordinates,
							level=level)

	# print gates at grid layer 0
	# plot_grid_level(results_directory, width, height, x_gates=x_gates, y_gates=y_gates)

	plt.show()
	return

def plot_3D(results_directory, chip, width, height):

    # get all gates
    x_gates, y_gates = chip.get_gates_coordinates()
    all_paths_coordinates = chip.get_all_paths_coordinates()

    colors = ["b", "g", "c", "m", "y"]
    markers = [".", "^", ",", "v", "<", ">"]
    color_index = 0
    marker_index = 0

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # set ticks to step of 1 for correct grid
    x_ticks = range(width)
    y_ticks = range(height)
    z_ticks = range(chip.levels)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # set all ticks and labels off
    plt.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelbottom=False,
        labelleft=False)

    if all_paths_coordinates != None:
        for path_coordinates in all_paths_coordinates:
            prev_path_node_coordinate = path_coordinates[0]
            for path_node_coordinate in path_coordinates:
                ax.plot([path_node_coordinate[0],
                        prev_path_node_coordinate[0]],
                        [path_node_coordinate[1],
                        prev_path_node_coordinate[1]],
                        [path_node_coordinate[2],
                        prev_path_node_coordinate[2]],
                        color=colors[color_index],
                        marker=markers[marker_index],
                        markersize=5)
                prev_path_node_coordinate = path_node_coordinate
            color_index = (color_index + 1) % len(colors)
            marker_index = (marker_index + 1) % len(markers)

    	# xs = [point[0] for path_coordinates in all_paths_coordinates for point in path_coordinates]
    	# ys = [point[1] for path_coordinates in all_paths_coordinates for point in path_coordinates]
    	# zs = [point[2] for path_coordinates in all_paths_coordinates for point in path_coordinates]

    # plot gates if provided
    if (x_gates and y_gates) != None:
        ax.plot(x_gates, y_gates, [0 for i in range(len(x_gates))], 'ro', markersize=10)

    # ax.scatter(xs, ys, zs)
    # set correct limits and initiate grid
    ax.set_xlim(-1, width)
    ax.set_ylim(-1, height)
    ax.set_zlim(-1, chip.levels)
    plt.gca().invert_yaxis()        # invert the y-axis to get correct view
    ax.set_axis_off()
    plt.savefig(results_directory + "/plot_grid/plot_3D.png")
    plt.show()

# plot single grid layer
def plot_grid_level(results_directory, width, height, all_paths_coordinates=None,
                    x_gates=None, y_gates=None, level=0):

    colors = ["b", "g", "c", "m", "y"]
    markers = [".", "^", ",", "v", "<", ">"]
    color_index = 0
    marker_index = 0

    fig, ax = plt.subplots()
    x_ticks = range(width)      # set ticks to step of 1 for correct grid
    y_ticks = range(height)     # set ticks to step of 1 for correct grid
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    # set all ticks and labels off
    plt.tick_params(
        axis="both",
        which="both",
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelbottom=False,
        labelleft=False)

    # plot all paths at current level if provided
    if all_paths_coordinates != None:
        for path_coordinates in all_paths_coordinates:
            prev_path_node_coordinate = path_coordinates[0]
            for path_node_coordinate in path_coordinates:
                if path_node_coordinate[2] == level:
                    ax.plot([path_node_coordinate[0],
                            prev_path_node_coordinate[0]],
                            [path_node_coordinate[1],
                            prev_path_node_coordinate[1]],
                            color=colors[color_index],
                            marker=markers[marker_index])
                prev_path_node_coordinate = path_node_coordinate
            color_index = (color_index + 1) % len(colors)
            marker_index = (marker_index + 1) % len(markers)

    # plot gates if provided
    if (x_gates and y_gates) != None:
        ax.plot(x_gates, y_gates, 'ro')

    # set correct limits and initiate grid
    ax.set_xlim(-1, width)
    ax.set_ylim(-1, height)
    plt.gca().invert_yaxis()        # invert the y-axis to get correct view
    ax.grid(alpha=1)
    plt.savefig(results_directory + "/plot_grid/plot_grid" + str(level) + ".png")

    return