import pygame

import src.graphique.animation as animation

vector=pygame.math.Vector2

class Player(animation.AnimateSprite):
    
    def __init__(self,x,y,walls):
        super().__init__("walk and idle","cat kigurumi walk and idle",self,x,y)
        self.feet=pygame.Rect(0,0,self.rect.width*0.5,12)
        self.walls=walls

        self.HORIZONTAL_ACCELERATION=0.4
        self.HORIZONTAL_FRICTION=0.2

        self.speed_player = 0.9
        self.is_moving = False
        self.position=vector(x,y)
        self.velocity=vector(0,0)
        self.acceleration=vector(0,0)
        
    def move_right(self):
        self.acceleration.x = self.HORIZONTAL_ACCELERATION
        self.direction_player = 'right'
        self.is_moving = True

    def move_left(self):
        self.acceleration.x = -self.HORIZONTAL_ACCELERATION  
        self.direction_player = 'left'
        self.is_moving = True

    def move_up(self):
        self.acceleration.y = -self.HORIZONTAL_ACCELERATION
        self.is_moving = True

    def move_down(self):
        self.acceleration.y = self.HORIZONTAL_ACCELERATION
        self.is_moving = True
        
    def stop_moving(self):
        self.is_moving = False
       
    def get_image(self, row, frame):
        image = pygame.Surface([24, 24],pygame.SRCALPHA)
        image.blit(self.sprite_sheet1, (0, 0), (frame * 24, row * 24, 24, 24))
        image.blit(self.sprite_sheet2, (0, 0), (frame * 24, row * 24, 24, 24))
        return image

    def update(self):

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
        self.check_movement_player()
        self.animate_player()
        
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