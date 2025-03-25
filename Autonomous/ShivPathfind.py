import numpy as np
import math
import heapq
import matplotlib.pyplot as plt


class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent row index
        self.parent_j = 0  # Parent column index
        self.f = float('inf')  # Total cost (g + h)
        self.g = float('inf')  # Cost from start to current cell
        self.h = 0  # Heuristic cost to destination


def load_map_from_file(filename):
    """Load map data from text file and return as numpy array"""
    with open(filename, "r") as f:
        # Skip header line with column numbers
        header = f.readline().strip()

        # Read remaining lines
        rows = []
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            # Skip row number (first element) and convert to integers
            row_data = [int(x) for x in parts[1:]]
            rows.append(row_data)

        # Convert to numpy array
        return np.array(rows)


def is_valid(grid, row, col):
    """Check if cell is within grid boundaries"""
    return (0 <= row < grid.shape[0]) and (0 <= col < grid.shape[1])


def is_unblocked(grid, row, col):
    """Check if cell is traversable (0 = open, 1 = blocked)"""
    return grid[row][col] == 0


def calculate_h_value(row, col, dest):
    """Calculate Euclidean distance heuristic"""
    return math.sqrt((row - dest[0]) ** 2 + (col - dest[1]) ** 2)

pathOut = np.empty
def trace_path(cell_details, dest):
    """Reconstruct path from destination to start"""
    path = []
    global pathOut
    row, col = dest
    pathOut = np.copy(dest)

    # Backtrack from destination to start
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        pathOut = np.vstack((pathOut, [row, col]))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j


        # temp_row = cell_details[row][col].parent_i
        # temp_col = cell_details[row][col].parent_j
        # row = temp_row
        # col = temp_col

    path.append((row, col))  # Add start position
    path.reverse()  # Reverse to get start-to-destination
    pathOut = np.vstack((pathOut, [row, col]))
    # Reverse the path to get the path from source to destination
    pathOut = np.delete(pathOut, 0, 0)
    pathOut = np.flip(pathOut, axis=0)


    print("\nPath found with", len(path), "steps:")
    for i, (r, c) in enumerate(path):

        print(f"Step {i + 1}: ({r}, {c})")

    return path


def a_star_search(grid, src, dest):
    """Perform A* pathfinding on the grid"""
    # Validate inputs
    if not (is_valid(grid, src[0], src[1]) and is_valid(grid, dest[0], dest[1])):
        print("Error: Source or destination outside map bounds")
        return None

    if not (is_unblocked(grid, src[0], src[1]) and is_unblocked(grid, dest[0], dest[1])):
        print("Error: Source or destination is blocked")
        return None

    if src == dest:
        print("Already at destination")
        return [tuple(src)]

    # Initialize data structures
    rows, cols = grid.shape
    closed_list = np.zeros((rows, cols), dtype=bool)
    cell_details = [[Cell() for _ in range(cols)] for _ in range(rows)]

    # Initialize start node
    i, j = src
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Possible movement directions (4 cardinal + 4 diagonal)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    while open_list:
        _, i, j = heapq.heappop(open_list)
        closed_list[i][j] = True

        # Check all possible movements
        for di, dj in directions:
            ni, nj = i + di, j + dj

            if is_valid(grid, ni, nj) and is_unblocked(grid, ni, nj) and not closed_list[ni][nj]:
                if [ni, nj] == dest:  # Found destination
                    cell_details[ni][nj].parent_i = i
                    cell_details[ni][nj].parent_j = j
                    return trace_path(cell_details, dest)

                # Calculate movement cost (1.0 for cardinal, 1.414 for diagonal)
                move_cost = 1.0 if di == 0 or dj == 0 else 1.414
                g_new = cell_details[i][j].g + move_cost
                h_new = calculate_h_value(ni, nj, dest)
                f_new = g_new + h_new

                # Update cell if we found a better path
                if f_new < cell_details[ni][nj].f:
                    heapq.heappush(open_list, (f_new, ni, nj))
                    cell_details[ni][nj].f = f_new
                    cell_details[ni][nj].g = g_new
                    cell_details[ni][nj].h = h_new
                    cell_details[ni][nj].parent_i = i
                    cell_details[ni][nj].parent_j = j

    print("No valid path found to destination")
    return None


def visualize_path(grid, path):
    """Create a matplotlib visualization of the path"""
    plt.figure(figsize=(12, 12))

    # Create colormap: black for 0 (open), white for 1 (blocked)
    cmap = plt.cm.colors.ListedColormap(['black', 'white'])
    plt.imshow(grid, cmap=cmap, interpolation='none')

    if path:
        # Extract coordinates (note matplotlib uses (x,y) = (col,row))
        y_coords = [coord[0] for coord in path]
        x_coords = [coord[1] for coord in path]

        # Plot path
        plt.scatter(x_coords, y_coords, color='yellow', s=100, marker='s',
                    edgecolor='red', linewidth=1, label='Path')
        plt.plot(x_coords, y_coords, 'r-', linewidth=2, alpha=0.5)

        # Mark start and end
        plt.scatter(x_coords[0], y_coords[0], color='lime', s=150,
                    marker='o', edgecolor='black', linewidth=2, label='Start')
        plt.scatter(x_coords[-1], y_coords[-1], color='magenta', s=150,
                    marker='X', edgecolor='black', linewidth=2, label='End')

    plt.axis('off')
    plt.title('A* Pathfinding Visualization (0s = traversable)', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1.15))
    plt.tight_layout()
    plt.show()


def main(src,dest):
    # ====== INPUT PARAMETERS ======
    # Define all your inputs here instead of using console input

    # Map file to load
    map_file = "ResizedMap_pooled_2x2.txt"

    # Start and destination coordinates (row, column)


    # Visualization flag
    show_visualization = True  # Set to False to disable visualization

    # ====== MAIN EXECUTION ======
    print("A* Pathfinding on Grid Map\n" + "=" * 30)
    print("Now treating 0s as traversable and 1s as blocked\n")
    print(f"Start: {src}, Destination: {dest}")

    # Load map
    try:
        grid = load_map_from_file(map_file)
        print(f"Successfully loaded map with dimensions: {grid.shape}")
    except Exception as e:
        print(f"Error loading map file: {e}")
        return

    # Display map info
    print("\nMap summary:")
    print(f"Total cells: {grid.size}")
    print(f"Traversable cells (0): {np.sum(grid == 0)}")
    print(f"Blocked cells (1): {np.sum(grid == 1)}")

    # Run A* search
    print("\nFinding path...")
    path = a_star_search(grid, src, dest)

    print("path: \n", pathOut)
    # Visualize if path was found and visualization is enabled
    # if path and show_visualization:
    #     visualize_path(grid, path)


if __name__ == "__main__":
    src = [29, 129]  # Starting position (row, column)
    dest = [284, 393]  # Destination position
    main(src,dest)
