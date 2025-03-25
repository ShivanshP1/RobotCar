import numpy as np
import math
import heapq
import matplotlib.pyplot as plt
from enum import Enum

class Direction(Enum):
    UP = 0    # -row
    RIGHT = 1 # +col
    DOWN = 2  # +row
    LEFT = 3  # -col

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0
        self.direction = None  # Direction from parent
        self.driving_side = None  # Which side of road we're on

def load_map_from_file(filename):
    with open(filename, "r") as f:
        header = f.readline().strip()
        rows = []
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            row_data = [int(x) for x in parts[1:]]
            rows.append(row_data)
        return np.array(rows)

def is_valid(grid, row, col):
    return (0 <= row < grid.shape[0]) and (0 <= col < grid.shape[1])

def is_unblocked(grid, row, col):
    return grid[row][col] == 0

def calculate_h_value(row, col, dest):
    return math.sqrt((row - dest[0])**2 + (col - dest[1])**2)

def get_road_direction(grid, row, col):
    """Determine primary road direction at this cell"""
    directions = []
    if is_valid(grid, row-1, col) and is_unblocked(grid, row-1, col):
        directions.append(Direction.UP)
    if is_valid(grid, row+1, col) and is_unblocked(grid, row+1, col):
        directions.append(Direction.DOWN)
    if is_valid(grid, row, col-1) and is_unblocked(grid, row, col-1):
        directions.append(Direction.LEFT)
    if is_valid(grid, row, col+1) and is_unblocked(grid, row, col+1):
        directions.append(Direction.RIGHT)
    
    if not directions:
        return Direction.RIGHT  # Default if isolated
    return max(directions, key=lambda x: directions.count(x))

def get_driving_side(row, col, direction):
    """Returns whether we're on right side (True) or left side (False)"""
    # Right side is our right when facing in the road direction
    if direction == Direction.UP:
        return (row, col-1)  # Right side is to our left (col-1)
    elif direction == Direction.RIGHT:
        return (row-1, col)  # Right side is above us (row-1)
    elif direction == Direction.DOWN:
        return (row, col+1)  # Right side is to our right (col+1)
    elif direction == Direction.LEFT:
        return (row+1, col)  # Right side is below us (row+1)

def is_proper_driving_side(current_dir, new_dir, move_dir):
    """Check if movement follows right-side driving rules"""
    if current_dir is None:
        return True  # Starting movement
    
    # Driving priority: straight > right turn > left turn > U-turn
    if new_dir == current_dir:
        return True  # Straight
    elif (current_dir.value + 1) % 4 == new_dir.value:
        return True  # Right turn
    elif (current_dir.value - 1) % 4 == new_dir.value:
        return False  # Left turn
    else:
        return False  # U-turn

def get_direction_from_move(di, dj):
    if di == -1 and dj == 0:
        return Direction.UP
    elif di == 1 and dj == 0:
        return Direction.DOWN
    elif di == 0 and dj == -1:
        return Direction.LEFT
    elif di == 0 and dj == 1:
        return Direction.RIGHT
    return None

def trace_path(cell_details, dest):
    path = []
    row, col = dest
    
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col, cell_details[row][col].direction, 
                    cell_details[row][col].driving_side))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j
    
    path.append((row, col, None, None))
    path.reverse()
    
    print("\nPath found with", len(path), "steps:")
    for i, (r, c, d, side) in enumerate(path):
        side_str = "RIGHT" if side else "LEFT" if side is not None else "START"
        dir_str = d.name if d is not None else "START"
        print(f"Step {i+1}: ({r}, {c}) facing {dir_str} ({side_str} side)")
    
    return [(r, c) for r, c, d, side in path]

def a_star_search(grid, src, dest, strict_rules=True):
    if not (is_valid(grid, src[0], src[1]) and is_valid(grid, dest[0], dest[1])):
        print("Error: Source or destination outside map bounds")
        return None
    
    if not (is_unblocked(grid, src[0], src[1]) and is_unblocked(grid, dest[0], dest[1])):
        print("Error: Source or destination is blocked")
        return None
    
    if src == dest:
        print("Already at destination")
        return [tuple(src)]
    
    rows, cols = grid.shape
    closed_list = np.zeros((rows, cols), dtype=bool)
    cell_details = [[Cell() for _ in range(cols)] for _ in range(rows)]
    
    i, j = src
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j
    cell_details[i][j].direction = get_road_direction(grid, i, j)
    cell_details[i][j].driving_side = True  # Assume starting on right side
    
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))
    
    # 4-directional movement (no diagonals for proper driving)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    
    while open_list:
        _, i, j = heapq.heappop(open_list)
        closed_list[i][j] = True
        
        current_dir = cell_details[i][j].direction
        current_side = cell_details[i][j].driving_side
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            
            if is_valid(grid, ni, nj) and is_unblocked(grid, ni, nj) and not closed_list[ni][nj]:
                move_dir = get_direction_from_move(di, dj)
                new_dir = get_road_direction(grid, ni, nj)
                
                # Determine driving side for new position
                right_side_pos = get_driving_side(ni, nj, new_dir)
                new_side = (ni, nj) == right_side_pos
                
                # Calculate movement cost with driving rules
                move_cost = 1.0  # Base cost
                
                if strict_rules:
                    # Penalize wrong-side driving
                    if not new_side:
                        move_cost += 5.0  # Heavy penalty for wrong side
                    
                    # Penalize non-preferred turns
                    if not is_proper_driving_side(current_dir, new_dir, move_dir):
                        move_cost += 2.0  # Penalty for bad turns
                
                g_new = cell_details[i][j].g + move_cost
                h_new = calculate_h_value(ni, nj, dest)
                f_new = g_new + h_new
                
                if [ni, nj] == dest:
                    cell_details[ni][nj].parent_i = i
                    cell_details[ni][nj].parent_j = j
                    cell_details[ni][nj].direction = new_dir
                    cell_details[ni][nj].driving_side = new_side
                    return trace_path(cell_details, dest)
                
                if f_new < cell_details[ni][nj].f:
                    heapq.heappush(open_list, (f_new, ni, nj))
                    cell_details[ni][nj].f = f_new
                    cell_details[ni][nj].g = g_new
                    cell_details[ni][nj].h = h_new
                    cell_details[ni][nj].parent_i = i
                    cell_details[ni][nj].parent_j = j
                    cell_details[ni][nj].direction = new_dir
                    cell_details[ni][nj].driving_side = new_side
    
    # If strict rules failed, try without them
    if strict_rules:
        print("Retrying without strict driving rules...")
        return a_star_search(grid, src, dest, strict_rules=False)
    
    print("Error: No valid path exists between source and destination")
    return None

def visualize_path(grid, path):
    plt.figure(figsize=(12, 12))
    cmap = plt.cm.colors.ListedColormap(['black', 'white'])
    plt.imshow(grid, cmap=cmap, interpolation='none')
    
    if path:
        y_coords = [coord[0] for coord in path]
        x_coords = [coord[1] for coord in path]
        
        # Plot path with color indicating driving side
        for i in range(len(path)-1):
            r, c = path[i]
            nr, nc = path[i+1]
            # Determine if this segment is on right side
            direction = get_road_direction(grid, r, c)
            right_side_pos = get_driving_side(r, c, direction)
            on_right = (r, c) == right_side_pos
            
            color = 'limegreen' if on_right else 'orange'
            plt.plot([c, nc], [r, nr], color=color, linewidth=3, alpha=0.7)
        
        # Markers for start and end
        plt.scatter(x_coords[0], y_coords[0], color='blue', s=200,
                    marker='o', edgecolor='black', linewidth=2, label='Start')
        plt.scatter(x_coords[-1], y_coords[-1], color='red', s=200,
                    marker='X', edgecolor='black', linewidth=2, label='End')
    
    plt.axis('off')
    plt.title('A* Pathfinding with Right-Side Driving', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1.15))
    plt.tight_layout()
    plt.show()

def main():
    # ====== INPUT PARAMETERS ======
    map_file = "ResizedMap_pooled_2x2.txt"
    src = [29, 129]    # Starting position (row, column)
    dest = [284,393]  # Destination position (row, column)
    show_visualization = True
    strict_driving_rules = True
    
    # ====== MAIN EXECUTION ======
    print("A* Pathfinding with Proper Right-Side Driving\n" + "="*50)
    print(f"Start: {src}, Destination: {dest}")
    
    try:
        grid = load_map_from_file(map_file)
        print(f"Loaded map with dimensions: {grid.shape}")
    except Exception as e:
        print(f"Error loading map file: {e}")
        return
    
    print("\nFinding path with proper right-side driving...")
    path = a_star_search(grid, src, dest, strict_rules=strict_driving_rules)
    
    if path and show_visualization:
        visualize_path(grid, path)

if __name__ == "__main__":
    main()