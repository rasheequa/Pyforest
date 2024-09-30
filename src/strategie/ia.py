import math
import pygame
vector = pygame.math.Vector2

class IA:
    def __init__(self, mob, player):
        self.mob = mob
        self.player = player
        self.metre = 16
        self.pixel = 16
        self.radius = self.pixel * self.metre
        self.min_distance = 5

        self.last_move_time = pygame.time.get_ticks()

        self.max_speed = 3  
        self.min_speed = 1 

    def update(self):

        dx = self.player.position.x - self.mob.position.x
        dy = self.player.position.y - self.mob.position.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if self.min_distance < distance < self.radius:
           
            direction_x = dx / distance if distance != 0 else 0
            direction_y = dy / distance if distance != 0 else 0


            self.mob.acceleration = vector(direction_x , direction_y)

            if direction_x > 0:
                self.mob.move_right()
            else:
                self.mob.move_left()

            if direction_y > 0:
                self.mob.move_down()
            else:
                self.mob.move_up()

