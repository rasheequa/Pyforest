import pygame
import animation
class Player(animation.AnimateSprite):
    
    def __init__(self,x,y):
        super().__init__("walk and idle","cat kigurumi walk and idle",x,y)

    def move_right(self):
        self.position[0] += self.speed
        self.direction = 'right'
        self.is_moving = True

    def move_left(self):
        self.position[0] -= self.speed
        self.direction = 'left'
        self.is_moving = True

    def move_up(self):
        self.position[1] -= self.speed
        self.is_moving = True

    def move_down(self):
        self.position[1] += self.speed
        self.is_moving = True
        
    def stop_moving(self):
        self.is_moving = False
       
    def get_image(self, row, frame):
        image = pygame.Surface([24, 24],pygame.SRCALPHA)
        image.blit(self.sprite_sheet1, (0, 0), (frame * 24, row * 24, 24, 24))
        image.blit(self.sprite_sheet2, (0, 0), (frame * 24, row * 24, 24, 24))
        return image

    def update(self):
        self.rect.topleft = self.position
        self.check_movement()
        self.animate()