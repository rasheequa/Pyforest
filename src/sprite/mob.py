import time
import pygame
import src.graphique.animation as animation
vector=pygame.math.Vector2

class Mob(animation.AnimateSprite):
    
    def __init__(self, x, y,walls):
        super().__init__("blue mushroom sheet", None, x, y)
        
        self.old_position = self.position.copy()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.walls=walls
        self.position = vector(x, y)  
        self.velocity = vector(0, 0) 
        self.acceleration = vector(0, 0)
        
        self.HORIZONTAL_ACCELERATION = 0.1  
        self.HORIZONTAL_FRICTION = 0.2
        
    def save_location(self): 
        self.old_position = self.position.copy()
        
    def move_right(self):
        self.acceleration.x = self.HORIZONTAL_ACCELERATION 
        self.direction = 'right'

    def move_left(self):
        self.acceleration.x = -self.HORIZONTAL_ACCELERATION 
        self.direction = 'left'

    def move_up(self):
        self.acceleration.y = -self.HORIZONTAL_ACCELERATION  

    def move_down(self):
        self.acceleration.y = self.HORIZONTAL_ACCELERATION  
        
    def stop_moving(self):
        self.acceleration = pygame.math.Vector2(0, 0)  

    def get_image(self, row, frame):
        image = pygame.Surface([24, 24], pygame.SRCALPHA)
        image.blit(self.sprite_sheet1, (0, 0), (frame * 16, row * 16, 16, 16))
        if hasattr(self, 'sprite_sheet2'):
            image.blit(self.sprite_sheet2, (0, 0), (frame * 24, row * 24, 24, 24))
        return image
    
    def update(self):
        self.save_location()  

        self.velocity += self.acceleration
        self.velocity.x *= (1 - self.HORIZONTAL_FRICTION)
        self.velocity.y *= (1 - self.HORIZONTAL_FRICTION)

     
        future_position = self.position + self.velocity

  
        self.position.x = future_position.x
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

       
        self.check_collision(axis='x')

  
        self.position.y = future_position.y
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

     
        self.check_collision(axis='y')

        self.acceleration = vector(0, 0)
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.check_movement()
        self.animate_player()
        
    def check_collision(self, axis):
        """
        Checks for collisions with the list of obstacles.
        Adjusts the player's position if a collision is detected.
        """
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