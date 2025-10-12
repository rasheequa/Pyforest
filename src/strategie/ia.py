import heapq
import math
import random
import pygame
vector=pygame.Vector2
import time
import pygame
import pytmx
import pyscroll
import pytmx.util_pygame

class IA:
    def __init__(self, mob, player, tiled_map):
        print(f"[IA INIT] Création IA pour mob à {mob.position}")
        self.mob = mob
        self.player = player
        self.tiled_map = tiled_map

        self.pixel = 16
        self.radius = self.pixel * 8  # Increased from 2 to 8 tiles (128 pixels)
        self.idle_radius = self.pixel * 7

        self.last_move_time = pygame.time.get_ticks()

        self.min_distance = 5  
        self.is_idling=True
        self.steps = 0
        self.step_count = 0
        self.random_direction = ''
        self.spawn_pos = self.mob.position.copy()

        self.astar = AStar(self.tiled_map)
        self.current_path = None
        self.last_player_grid = None
        self.last_recalc_time = 0
        self.recalc_cooldown = 250  # ms between forced path recalculations

    def update(self):
        mob_pos = (int(self.mob.position.x // self.pixel), int(self.mob.position.y // self.pixel))
        player_center = self.player.rect.center
        player_pos = (int(player_center[0] // self.pixel), int(player_center[1] // self.pixel))

        # print(f"[AI DEBUG] Mob id {id(self.mob)} grid: {mob_pos}, Player grid: {player_pos}, Mob pos: {self.mob.position}, Player rect.center: {player_center}")

        player_vec = vector(player_center[0], player_center[1])
        distance_to_player = self.mob.position.distance_to(player_vec)
        can_see_player = True  # LOS désactivé temporairement
        # print(f"[AI DEBUG] Mob id {id(self.mob)} distance_to_player: {distance_to_player}, can_see_player: {can_see_player}")
        
        # More informative debug message about pathfinding decisions
        # if distance_to_player <= self.radius:
        #     if distance_to_player <= self.pixel * 1.5:
        #         print(f"[AI DEBUG] Mob id {id(self.mob)} trop proche du joueur ({distance_to_player:.2f} pixels), pas de recalcul de chemin")
        #     else:
        #         print(f"[AI DEBUG] Mob id {id(self.mob)} dans le rayon de poursuite, recalcul du chemin")

        # Don't recalculate path if too close to player (within 1.5 tiles)
        min_recalc_distance = self.pixel * 1.5

        now = pygame.time.get_ticks()

        # Pursuit: mobs follow the player if in radius, but don't recalculate when too close
        if distance_to_player <= self.radius:
            # When very close, just stop
            if distance_to_player <= min_recalc_distance:
                self.mob.velocity = vector(0, 0)
                self.mob.speed_mob = 1.1
            else:
                # Only recalculate path when player moved to a different grid or cooldown expired
                need_recalc = False
                if self.last_player_grid != player_pos:
                    need_recalc = True
                if now - self.last_recalc_time > self.recalc_cooldown:
                    need_recalc = True

                if need_recalc:
                    goal_node = Node(player_pos)
                    start_node = Node(mob_pos)
                    path = self.astar.search(start_node, goal_node)
                    self.last_recalc_time = now
                    self.last_player_grid = player_pos
                    self.current_path = path

                if self.current_path:
                    # Mob poursuit le joueur à vitesse modérée
                    self.mob.speed_mob = 1.4
                    self.move_along_path(self.current_path)
        elif distance_to_player > self.radius:
            # Retour à la position de spawn à vitesse réduite
            self.mob.speed_mob = 1.1
            spawn_grid_pos = (int(self.spawn_pos.x // self.pixel), int(self.spawn_pos.y // self.pixel))
            goal_node = Node(spawn_grid_pos)
            start_node = Node(mob_pos)
            path = self.astar.search(start_node, goal_node)
            if path:
                self.move_along_path(path)
        else:
            self.mob.speed_mob = 2
            self.idle_movement()

    def line_of_sight(self, start, end):
        """
        Returns True if there is a clear line of sight between start and end (no obstacles).
        Uses Bresenham's line algorithm for grid-based LOS.
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
                    # print(f"[LOS DEBUG] Blocked at {(x, y)}")
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
                    # print(f"[LOS DEBUG] Blocked at {(x, y)}")
                    return False
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        # Check the final position
        if (x1, y1) in self.astar.obstacle_positions:
            # print(f"[LOS DEBUG] Blocked at {(x1, y1)} (final)")
            return False
        return True

    def move_along_path(self, path):
        if not hasattr(self, '_stuck_counter'):
            self._stuck_counter = 0
            self._last_node = None

        # Pop all nodes that are obstacles or current mob grid
        while path and (path[0] in self.astar.obstacle_positions or path[0] == (int(self.mob.position.x // self.pixel), int(self.mob.position.y // self.pixel))):
            # print(f"[AI DEBUG] On pop le nœud bloqué ou déjà atteint: {path[0]}")
            path.pop(0)
        if not path:
            self.mob.velocity = vector(0, 0)
            return

        next_pos = path[0]
        next_pixel_pos = vector(next_pos[0] * self.pixel, next_pos[1] * self.pixel)
        direction = next_pixel_pos - self.mob.position
        if direction.length() > 0:
            direction = direction.normalize()
            self.mob.velocity = direction * self.mob.speed_mob
        else:
            self.mob.velocity = vector(0, 0)

        # If mob is not making progress toward the node, increment stuck counter
        if self._last_node == next_pos:
            if self.mob.position.distance_to(next_pixel_pos) > self.mob.speed_mob * 2:
                self._stuck_counter += 1
            else:
                self._stuck_counter = 0
        else:
            self._stuck_counter = 0
        self._last_node = next_pos

        # Pop node if close enough or stuck for several frames
        if self.mob.position.distance_to(next_pixel_pos) < self.mob.speed_mob or self._stuck_counter > 10:
            # print(f"[AI DEBUG] On pop le nœud car trop proche ou bloqué: {next_pos}")
            path.pop(0)
            self._stuck_counter = 0

    def idle_movement(self):
        # Idle movement behavior
        pass

class Node:
    def __init__(self, pos, g_cost=0, h_cost=0, parent=None):
        self.pos = pos  
        self.g_cost = g_cost 
        self.h_cost = h_cost  
        self.f_cost = g_cost + h_cost  
        self.parent = parent  

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __hash__(self):
        return hash(self.pos)
    
class AStar:
    def __init__(self, map_grid):
        self.open = [] 
        self.closed = []  
        self.map_grid = map_grid

        self.obstacle_positions = set()
        for obj in self.map_grid.objects:
            if obj.type == 'collision':
                grid_x = int(obj.x // self.map_grid.tilewidth)
                grid_y = int(obj.y // self.map_grid.tileheight)
                # Mark all tiles covered by the collision rect as obstacles
                width = int(obj.width // self.map_grid.tilewidth)
                height = int(obj.height // self.map_grid.tileheight)
                for dx in range(width if width > 0 else 1):
                    for dy in range(height if height > 0 else 1):
                        self.obstacle_positions.add((grid_x + dx, grid_y + dy))

    def search(self, start_node, goal_node):
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

            if current_node.pos == goal_node.pos:
                return self.reconstruct_path(current_node)

            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                if neighbor.pos in closed_set:
                    continue

                g_cost = current_node.g_cost + 1
                h_cost = self.heuristic(neighbor, goal_node)
                f_cost = g_cost + h_cost

                if neighbor.pos not in node_map or g_cost < node_map[neighbor.pos].g_cost:
                    # Always use the same Node object for each position
                    if neighbor.pos not in node_map:
                        node_map[neighbor.pos] = neighbor
                    node = node_map[neighbor.pos]
                    self.update_node(node, g_cost, h_cost, current_node)
                    if neighbor.pos not in open_set:
                        heapq.heappush(open_list, (node.f_cost, node))
                        open_set.add(neighbor.pos)

        return None

    def get_neighbors(self, node):
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
        return abs(node.pos[0] - goal.pos[0]) + abs(node.pos[1] - goal.pos[1])

    def reconstruct_path(self, node):
        path = []
        current = node

        while current:
            path.append(current.pos)
            current = current.parent

        return path[::-1] 

    def update_node(self, node, g_cost, h_cost, current_node):
        node.g_cost = g_cost
        node.h_cost = h_cost
        node.f_cost = g_cost + h_cost
        node.parent = current_node