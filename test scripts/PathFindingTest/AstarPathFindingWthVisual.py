import numpy as np
import math
import heapq

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

def load_map_from_file(filename):
    """Load map data from text file and return as numpy array"""
    with open(filename, "r") as f:
        # Read and process first line to get column headers
        header = f.readline().strip()
        cols = [int(x) for x in header.split()[1:]]  # Skip first empty space
        
        # Read remaining lines
        rows = []
        row_indices = []
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            row_idx = int(parts[0])
            row_data = [int(x) for x in parts[1:]]
            row_indices.append(row_idx)
            rows.append(row_data)
        
        # Convert to numpy array
        map_arr = np.array(rows)
        
        # Verify dimensions match headers
        if len(cols) != map_arr.shape[1]:
            print(f"Warning: Column count mismatch. Header suggests {len(cols)} columns, found {map_arr.shape[1]}")
        
        return map_arr

def is_valid(grid, row, col):
    return (row >= 0) and (row < grid.shape[0]) and (col >= 0) and (col < grid.shape[1])

def is_unblocked(grid, row, col):
    return grid[row][col] == 1

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def calculate_h_value(row, col, dest):
    return math.sqrt((row - dest[0]) ** 2 + (col - dest[1]) ** 2)

def trace_path(cell_details, dest):
    path = []
    row, col = dest
    
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j
    
    path.append((row, col))
    path.reverse()
    
    print("Path found:")
    for i, (r, c) in enumerate(path):
        print(f"Step {i+1}: ({r}, {c})")
    return path

def a_star_search(grid, src, dest):
    if not is_valid(grid, src[0], src[1]) or not is_valid(grid, dest[0], dest[1]):
        print("Invalid source or destination")
        return None
    
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or destination is blocked")
        return None
    
    if is_destination(src[0], src[1], dest):
        print("Already at destination")
        return [(src[0], src[1])]
    
    rows, cols = grid.shape
    closed_list = [[False for _ in range(cols)] for _ in range(rows)]
    cell_details = [[Cell() for _ in range(cols)] for _ in range(rows)]
    
    i, j = src
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j
    
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                 (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    while open_list:
        _, i, j = heapq.heappop(open_list)
        closed_list[i][j] = True
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            
            if is_valid(grid, ni, nj) and is_unblocked(grid, ni, nj) and not closed_list[ni][nj]:
                if is_destination(ni, nj, dest):
                    cell_details[ni][nj].parent_i = i
                    cell_details[ni][nj].parent_j = j
                    return trace_path(cell_details, dest)
                
                g_new = cell_details[i][j].g + (1.0 if di == 0 or dj == 0 else 1.414)  # sqrt(2) for diagonal
                h_new = calculate_h_value(ni, nj, dest)
                f_new = g_new + h_new
                
                if cell_details[ni][nj].f == float('inf') or cell_details[ni][nj].f > f_new:
                    heapq.heappush(open_list, (f_new, ni, nj))
                    cell_details[ni][nj].f = f_new
                    cell_details[ni][nj].g = g_new
                    cell_details[ni][nj].h = h_new
                    cell_details[ni][nj].parent_i = i
                    cell_details[ni][nj].parent_j = j
    
    print("No path found to destination")
    return None

def main():
    # Load map dynamically from file
    map_file = "ResizedMap_pooled_2x2.txt"
    grid = load_map_from_file(map_file)
    
    print(f"Loaded map with dimensions: {grid.shape}")
    print("Sample of map data:")
    print(grid[:5, :5])  # Print first 5x5 portion of map
    
    # Get user input for source and destination
    print("\nEnter source coordinates (row, col):")
    src_row = int(input("Row: "))
    src_col = int(input("Col: "))
    
    print("\nEnter destination coordinates (row, col):")
    dest_row = int(input("Row: "))
    dest_col = int(input("Col: "))
    
    src = [src_row, src_col]
    dest = [dest_row, dest_col]
    
    # Run A* search
    path = a_star_search(grid, src, dest)
    
    # Visualization option
    if path and input("\nVisualize path? (y/n): ").lower() == 'y':
        visualize_path(grid, path)

def visualize_path(grid, path):
    """Simple text visualization of the path"""
    rows, cols = grid.shape
    max_rows_to_show = min(20, rows)
    max_cols_to_show = min(20, cols)
    
    # Get the portion of the path that fits in our display
    display_path = [(r, c) for (r, c) in path if r < max_rows_to_show and c < max_cols_to_show]
    
    print("\nMap Visualization (first 20x20 cells):")
    print("0 = blocked, 1 = open, * = path")
    
    for r in range(max_rows_to_show):
        for c in range(max_cols_to_show):
            if (r, c) in display_path:
                print("*", end=" ")
            else:
                print(grid[r][c], end=" ")
        print()

if __name__ == "__main__":
    main()
