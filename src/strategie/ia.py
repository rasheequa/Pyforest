import heapq
import math
import random
import pygame
vector = pygame.Vector2
import time
import pytmx
import pyscroll
import pytmx.util_pygame

class IA:
    def __init__(self, mob, player, tiled_map):
        # Connect the AI with the mob, the player, and the map
        self.mob = mob
        self.player = player
        self.tiled_map = tiled_map

        # Tile size in pixels
        self.pixel = 16
        # Detection radius for chasing (8 tiles = 128 pixels)
        self.radius = self.pixel * 8
        # Radius for idle movement (7 tiles = 112 pixels)
        self.idle_radius = self.pixel * 7

        # Used to control time between moves
        self.last_move_time = pygame.time.get_ticks()

        # Minimum distance before stopping
        self.min_distance = 5  
        self.is_idling = True
        self.steps = 0
        self.step_count = 0
        self.random_direction = ''
        # Remember spawn position for returning
        self.spawn_pos = self.mob.position.copy()

        # Create A* pathfinding system
        self.astar = AStar(self.tiled_map)
        self.current_path = None
        self.last_player_grid = None
        self.last_recalc_time = 0
        # Time between forced recalculations (in ms)
        self.recalc_cooldown = 250  

    def update(self):
        # Convert mob and player positions to grid coordinates
        mob_pos = (int(self.mob.position.x // self.pixel), int(self.mob.position.y // self.pixel))
        player_center = self.player.rect.center
        player_pos = (int(player_center[0] // self.pixel), int(player_center[1] // self.pixel))

        # Compute distance between mob and player
        player_vec = vector(player_center[0], player_center[1])
        distance_to_player = self.mob.position.distance_to(player_vec)
        can_see_player = True  # Line of sight temporarily disabled
        min_recalc_distance = self.pixel * 1.5

        now = pygame.time.get_ticks()

        # --- If the player is inside detection range ---
        if distance_to_player <= self.radius:
            # If very close, stop moving
            if distance_to_player <= min_recalc_distance:
                self.mob.velocity = vector(0, 0)
                self.mob.speed_mob = 1.1
            else:
                need_recalc = False
                # Recalculate if player moved
                if self.last_player_grid != player_pos:
                    need_recalc = True
                # Or if enough time passed
                if now - self.last_recalc_time > self.recalc_cooldown:
                    need_recalc = True

                # Compute a new path using A*
                if need_recalc:
                    goal_node = Node(player_pos)
                    start_node = Node(mob_pos)
                    path = self.astar.search(start_node, goal_node)
                    self.last_recalc_time = now
                    self.last_player_grid = player_pos
                    self.current_path = path

                # Follow the path if it exists
                if self.current_path:
                    self.mob.speed_mob = 1.4
                    self.move_along_path(self.current_path)

        # --- If the player is far away, return to spawn ---
        elif distance_to_player > self.radius:
            self.mob.speed_mob = 1.1
            spawn_grid_pos = (int(self.spawn_pos.x // self.pixel), int(self.spawn_pos.y // self.pixel))
            goal_node = Node(spawn_grid_pos)
            start_node = Node(mob_pos)
            path = self.astar.search(start_node, goal_node)
            if path:
                self.move_along_path(path)

        # --- Otherwise (default idle behavior) ---
        else:
            self.mob.speed_mob = 2
            self.idle_movement()

    def line_of_sight(self, start, end):
        """
        Check if there is a clear line of sight (no obstacle between start and end).
        Uses Bresenham's line algorithm for grid-based maps.
        """
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        if dx > dy:
            err = dx / 2.0
            while x != x1:
                if (x, y) in self.astar.obstacle_positions:
                    return False
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                if (x, y) in self.astar.obstacle_positions:
                    return False
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

        # Check the final tile
        if (x1, y1) in self.astar.obstacle_positions:
            return False
        return True

    def move_along_path(self, path):
        # Initialize variables if not already done
        if not hasattr(self, '_stuck_counter'):
            self._stuck_counter = 0
            self._last_node = None

        # Skip blocked or current tiles
        while path and (path[0] in self.astar.obstacle_positions or 
                        path[0] == (int(self.mob.position.x // self.pixel), int(self.mob.position.y // self.pixel))):
            path.pop(0)
        if not path:
            self.mob.velocity = vector(0, 0)
            return

        # Move toward the next position in the path
        next_pos = path[0]
        next_pixel_pos = vector(next_pos[0] * self.pixel, next_pos[1] * self.pixel)
        direction = next_pixel_pos - self.mob.position

        # Normalize and move in that direction
        if direction.length() > 0:
            direction = direction.normalize()
            self.mob.velocity = direction * self.mob.speed_mob
        else:
            self.mob.velocity = vector(0, 0)

        # Detect if the mob is stuck
        if self._last_node == next_pos:
            if self.mob.position.distance_to(next_pixel_pos) > self.mob.speed_mob * 2:
                self._stuck_counter += 1
            else:
                self._stuck_counter = 0
        else:
            self._stuck_counter = 0
        self._last_node = next_pos

        # Go to the next node if close enough or stuck for too long
        if self.mob.position.distance_to(next_pixel_pos) < self.mob.speed_mob or self._stuck_counter > 10:
            path.pop(0)
            self._stuck_counter = 0

    def idle_movement(self):
        # TODO: Add random or patrol movement when idle
        pass


# --- Node class used in A* pathfinding ---
class Node:
    def __init__(self, pos, g_cost=0, h_cost=0, parent=None):
        self.pos = pos          # Position (x, y) in grid
        self.g_cost = g_cost    # Cost from start node
        self.h_cost = h_cost    # Heuristic (estimated cost to goal)
        self.f_cost = g_cost + h_cost  # Total cost
        self.parent = parent    # Previous node in the path

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __hash__(self):
        return hash(self.pos)
    

# --- A* Pathfinding algorithm ---
class AStar:
    def __init__(self, map_grid):
        self.open = []    # Nodes to check
        self.closed = []  # Checked nodes
        self.map_grid = map_grid

        # Build the list of obstacles from Tiled map
        self.obstacle_positions = set()
        for obj in self.map_grid.objects:
            if obj.type == 'collision':
                grid_x = int(obj.x // self.map_grid.tilewidth)
                grid_y = int(obj.y // self.map_grid.tileheight)
                width = int(obj.width // self.map_grid.tilewidth)
                height = int(obj.height // self.map_grid.tileheight)
                for dx in range(width if width > 0 else 1):
                    for dy in range(height if height > 0 else 1):
                        self.obstacle_positions.add((grid_x + dx, grid_y + dy))

    def search(self, start_node, goal_node):
        # Priority queue and helper sets
        open_list = []
        open_set = set()
        closed_set = set()
        node_map = {start_node.pos: start_node}

        heapq.heappush(open_list, (start_node.f_cost, start_node))
        open_set.add(start_node.pos)

        while open_list:
            _, current_node = heapq.heappop(open_list)
            open_set.discard(current_node.pos)
            closed_set.add(current_node.pos)

            # Goal reached → reconstruct path
            if current_node.pos == goal_node.pos:
                return self.reconstruct_path(current_node)

            # Explore neighbors
            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor.pos in closed_set:
                    continue

                g_cost = current_node.g_cost + 1
                h_cost = self.heuristic(neighbor, goal_node)
                f_cost = g_cost + h_cost

                # If better path found, update node
                if neighbor.pos not in node_map or g_cost < node_map[neighbor.pos].g_cost:
                    if neighbor.pos not in node_map:
                        node_map[neighbor.pos] = neighbor
                    node = node_map[neighbor.pos]
                    self.update_node(node, g_cost, h_cost, current_node)
                    if neighbor.pos not in open_set:
                        heapq.heappush(open_list, (node.f_cost, node))
                        open_set.add(neighbor.pos)

        # No path found
        return None

    def get_neighbors(self, node):
        # Get the 4 neighboring cells (up, down, left, right)
        dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        neighbors = []
        for dir in dirs:
            neighbor_pos = (node.pos[0] + dir[0], node.pos[1] + dir[1])
            if (0 <= neighbor_pos[0] < self.map_grid.width and
                0 <= neighbor_pos[1] < self.map_grid.height):
                if neighbor_pos not in self.obstacle_positions:
                    neighbors.append(Node(neighbor_pos))
        return neighbors

    def heuristic(self, node, goal):
        # Manhattan distance heuristic
        return abs(node.pos[0] - goal.pos[0]) + abs(node.pos[1] - goal.pos[1])

    def reconstruct_path(self, node):
        # Build the path by following parent links
        path = []
        current = node
        while current:
            path.append(current.pos)
            current = current.parent
        return path[::-1]  # Reverse the path

    def update_node(self, node, g_cost, h_cost, current_node):
        # Update costs and parent for a node
        node.g_cost = g_cost
        node.h_cost = h_cost
        node.f_cost = g_cost + h_cost
        node.parent = current_node
