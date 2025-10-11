import time
import pygame
import src.graphique.animation as animation
vector = pygame.math.Vector2

class Mob(animation.AnimateSprite):

    def __init__(self, x, y, walls):
        super().__init__("blue mushroom sheet", None,self, x, y)
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.walls = walls
        
        self.HORIZONTAL_ACCELERATION = 0.1
        self.HORIZONTAL_FRICTION = 0.1

        self.speed_mob = 1.2  # Mob plus lent que le joueur
        self.is_moving = False

        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        self.spawn=self.position.copy()

    def set_acceleration(self,x,y):
        self.acceleration = vector(x, y)*self.HORIZONTAL_ACCELERATION

    def move_right(self):
        self.acceleration.x = self.HORIZONTAL_ACCELERATION
        self.direction_mob = 'right'

    def move_left(self):
        self.acceleration.x = -self.HORIZONTAL_ACCELERATION
        self.direction_mob = 'left'

    def move_up(self):
        self.acceleration.y = -self.HORIZONTAL_ACCELERATION  

    def move_down(self):
        self.acceleration.y = self.HORIZONTAL_ACCELERATION  

    def stop_moving(self):
        self.acceleration = vector(0, 0)  

    def get_image(self, row, frame):
        image = pygame.Surface([24, 24], pygame.SRCALPHA)
        image.blit(self.sprite_sheet1, (0, 0), (frame * 16, row * 16, 16, 16))
        if hasattr(self, 'sprite_sheet2'):
            image.blit(self.sprite_sheet2, (0, 0), (frame * 24, row * 24, 24, 24))
        return image 

    def update(self):
        # Move mob by velocity set by AI (no acceleration/friction)
        old_position = self.position.copy()
        future_position = self.position + self.velocity

        # Set movement state based on if there's any velocity at all
        self.is_moving = abs(self.velocity.x) > 0.01 or abs(self.velocity.y) > 0.01
        
        # Update direction based on movement
        if self.velocity.x > 0:
            self.direction_mob = 'right'
        elif self.velocity.x < 0:
            self.direction_mob = 'left'

        self.position.x = future_position.x
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        collided_x = self.check_collision(axis='x')

        self.position.y = future_position.y
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        collided_y = self.check_collision(axis='y')

        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.check_movement_mob()
        self.animate_mob()

        # Debug prints
        print(f"[MOB DEBUG] is_moving: {self.is_moving}, speed_mob: {self.speed_mob}, velocity: {self.velocity}")
        if collided_x or collided_y:
            print(f"[MOB DEBUG] Collision at {self.position}, from {old_position}, velocity: {self.velocity}")
        else:
            print(f"[MOB DEBUG] Moved to {self.position}, velocity: {self.velocity}")

    def check_collision(self, axis):
        for obstacle in self.walls:
            if self.rect.colliderect(obstacle):
                if axis == 'x':
                   
                    if self.velocity.x > 0: 
                        self.position.x = obstacle.left - self.rect.width  
                    elif self.velocity.x < 0: 
                        self.position.x = obstacle.right 
                elif axis == 'y':
             
                    if self.velocity.y > 0:
                        self.position.y = obstacle.top - self.rect.height
                    elif self.velocity.y < 0: 
                        self.position.y = obstacle.bottom 

            
                self.rect.topleft = self.position
                self.feet.midbottom = self.rect.midbottom
                return True 
        return False 