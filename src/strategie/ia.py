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
    def __init__(self, mob, player,tiled_map):
        self.mob = mob
        self.player = player
        self.tiled_map = tiled_map

        self.pixel = 16
        self.radius = self.pixel * 6
        self.idle_radius = self.pixel*7

        self.last_move_time = pygame.time.get_ticks()

        self.min_distance = 5  
        self.is_idling=True
        self.steps = 0
        self.step_count = 0
        self.random_direction = ''
        self.spawn_pos = self.mob.position.copy()

        self.astar = AStar(self.tiled_map)

    def update(self):
        
        mob_pos = (int(self.mob.position.x // self.pixel ), int(self.mob.position.y // self.pixel ))
        player_pos = (int(self.player.position.x // self.pixel), int(self.player.position.y // self.pixel ))

        distance_to_player = self.mob.position.distance_to(self.player.position)

        if distance_to_player <= self.radius:
            
            goal_node = Node(player_pos)
        else:
           
            spawn_grid_pos = (int(self.spawn_pos.x // self.pixel), int(self.spawn_pos.y // self.pixel))
            goal_node = Node(spawn_grid_pos)

        start_node = Node(mob_pos)
     
        path = self.astar.search(start_node, goal_node)
        
        if path:
            print(f"Path found: {path}")
            self.move_along_path(path)
        # else:
            # self.idle_movement()

    def move_along_path(self, path):
       
        next_pos = path[0]  
        next_pixel_pos = vector(next_pos[0]* self.pixel, next_pos[1]* self.pixel)
    
        direction = next_pixel_pos - self.mob.position
        if direction.length() > 0:
            direction = direction.normalize()
        self.mob.position += direction * self.mob.speed_mob

        if self.mob.position.distance_to(next_pixel_pos) < self.mob.speed_mob:
            path.pop(0)

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
            if obj.type == 'obstacle': 
                grid_x = int(obj.x// self.map_grid.tilewidth)
                grid_y = int(obj.y// self.map_grid.tileheight)
                self.obstacle_positions.add((grid_x, grid_y))

    def search(self, start_node, goal_node):
        open_list = []
        closed_list = set()


        heapq.heappush(open_list, start_node)

        while open_list:

            current_node = heapq.heappop(open_list)

            closed_list.add(current_node)

            if current_node == goal_node:
                return self.reconstruct_path(current_node)

            neighbors = self.get_neighbors(current_node)

            for neighbor in neighbors:
                if neighbor in closed_list:
                    continue

                g_cost = current_node.g_cost + 1 
                h_cost = self.heuristic(neighbor, goal_node)
                f_cost = g_cost + h_cost

                if neighbor in open_list:
                    if neighbor.f_cost > f_cost:
                        self.update_node(neighbor, g_cost, h_cost, current_node)
                else:
                    self.update_node(neighbor, g_cost, h_cost, current_node)
                    heapq.heappush(open_list, neighbor)

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