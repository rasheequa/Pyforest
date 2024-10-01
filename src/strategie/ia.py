import math
import random
import pygame
vector=pygame.Vector2

class IA:
    def __init__(self, mob, player):
        self.mob = mob
        self.player = player

        self.pixel = 16
        self.radius = self.pixel * 6
        self.idle_radius = self.pixel*7

        self.last_move_time = pygame.time.get_ticks()

        self.min_distance = 5
        self.max_speed = 3  
        self.min_speed = 1
        
        self.is_idling=True
        self.steps = 0
        self.step_count = 0
        self.random_direction = ''


    def get_distance_to_spawn(self):
        dx = self.mob.position.x - self.mob.spawn.x
        dy = self.mob.position.y - self.mob.spawn.y
        return math.sqrt(dx ** 2 + dy ** 2)
    
    def get_distance_to_player(self):
        dx = self.mob.position.x - self.player.position.x
        dy = self.mob.position.y - self.player.position.y
        return math.sqrt(dx ** 2 + dy ** 2)
    
    def is_within_spawn(self, x, y):
        dx = x - self.mob.spawn.x
        dy = y - self.mob.spawn.y
        distance_from_spawn = math.sqrt(dx ** 2 + dy ** 2)
        return distance_from_spawn <= self.idle_radius

    def is_within_player(self):
        distance_from_player = self.get_distance_to_player()
        return distance_from_player <= self.radius

    
    def update(self):
        
        if self.is_within_player() :
            self.is_idling = False
            self.pathfind_to_player()

        elif self.is_within_spawn(self.mob.position.x,self.mob.position.y):
            self.is_idling = True
            if self.step_count == 0:
                self.steps = 50
                self.random_direction = random.choice(['right', 'left', 'up', 'down'])
            
            if self.step_count < self.steps:
                if self.random_direction == 'right':
                    self.mob.set_acceleration(1, 0)
                    self.mob.move_right()
                elif self.random_direction == 'left':
                    self.mob.set_acceleration(-1, 0)
                    self.mob.move_left()
                elif self.random_direction == 'up':
                    self.mob.set_acceleration(0, -1)
                    self.mob.move_up()
                elif self.random_direction == 'down':
                    self.mob.set_acceleration(0,1)
                    self.mob.move_down()

                self.step_count += 1

            else:
                self.step_count = 0
                self.mob.stop_moving()
        
        else:
            self.return_to_spawn()



    def pathfind_to_player(self):

        dx = self.player.position.x - self.mob.position.x
        dy = self.player.position.y - self.mob.position.y

        distance_to_player = math.sqrt(dx ** 2 + dy ** 2)

        if self.min_distance < distance_to_player < self.radius:
            direction_x = dx / distance_to_player if distance_to_player != 0 else 0
            direction_y = dy / distance_to_player if distance_to_player != 0 else 0
            
            new_position_x = self.mob.position.x + direction_x * self.max_speed
            new_position_y = self.mob.position.y + direction_y * self.max_speed

            
            if self.is_within_spawn(new_position_x, new_position_y):
                self.mob.set_acceleration(direction_x* self.max_speed, direction_y* self.max_speed) 
                
                self.move_towards(direction_x, direction_y)
            else:
                self.return_to_spawn()
        else:
            self.mob.stop_moving()


    def move_towards(self, direction_x, direction_y):
        
        if direction_x > 0:
            self.mob.move_right()
        
        else:
            self.mob.move_left()

        if direction_y > 0:
            self.mob.move_down()
        else:
            self.mob.move_up()

    
    def return_to_spawn(self):

        dx = self.mob.spawn.x - self.mob.position.x
        dy = self.mob.spawn.y - self.mob.position.y
        distance_to_spawn = math.sqrt(dx ** 2 + dy ** 2)

        if distance_to_spawn > self.min_distance:
            direction_x = dx / distance_to_spawn if distance_to_spawn != 0 else 0
            direction_y = dy / distance_to_spawn if distance_to_spawn != 0 else 0
            self.mob.set_acceleration(direction_x* self.max_speed, direction_y* self.max_speed)
            self.move_towards(direction_x, direction_y)
        
        else:
            self.mob.stop_moving()