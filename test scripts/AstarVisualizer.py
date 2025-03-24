import matplotlib.pyplot as plt
import numpy as np

import pathFinding


def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Skip the first line (header with column numbers)
    data_lines = lines[1:]

    # Extract the data (skip the first element in each line which is the row number)
    data = []
    for line in data_lines:
        parts = line.strip().split()
        row_data = [int(x) for x in parts[1:]]  # Skip the row number
        data.append(row_data)

    return np.array(data)


def visualize_with_path(data, path_coords):
    plt.figure(figsize=(12, 12))

    # Create a colormap where 0 is white and 1 is black
    cmap = plt.cm.colors.ListedColormap(['white', 'black'])

    # Display the base data
    plt.imshow(data, cmap=cmap, interpolation='none')

    # Extract x and y coordinates from the path
    # Note: The coordinates in the file appear to be (row, column),
    # but matplotlib's imshow uses (column, row) for plotting
    y_coords = [coord[0] for coord in path_coords]
    x_coords = [coord[1] for coord in path_coords]

    # Plot the path as yellow squares
    plt.scatter(x_coords, y_coords, color='yellow', s=100, marker='s',
                edgecolor='red', linewidth=1, label='Path')

    # Connect the points with a line
    plt.plot(x_coords, y_coords, 'r-', linewidth=2, alpha=0.5)

    # Add markers for start and end points
    if len(path_coords) > 0:
        plt.scatter(x_coords[0], y_coords[0], color='lime', s=150,
                    marker='o', edgecolor='black', linewidth=2, label='Start')
        plt.scatter(x_coords[-1], y_coords[-1], color='magenta', s=150,
                    marker='X', edgecolor='black', linewidth=2, label='End')

    # Customize the plot
    plt.axis('off')
    plt.title('Path Visualization on Binary Map', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    plt.tight_layout()
    plt.show()


# Replace with your actual file path
filename = 'Resizedquackmap_pooled_3x3.txt'

# Read the base data
data = read_data(filename)

# The path coordinates (row, column) from your message

AstarPathFinding.main()
path_coords = AstarPathFinding.path
print(path_coords)


# Visualize the data with the path
visualize_with_path(data, path_coords)
