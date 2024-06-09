import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        super().__init__()
        self.sprite_sheet1 = pygame.image.load('Tiny Wonder Forest 1.0\characters\main character\walk and idle.png')
        self.sprite_sheet2 = pygame.image.load('Tiny Wonder Forest 1.0\characters\main character\cat kigurumi walk and idle.png')
        
        self.image= self.get_image(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect =self.image.get_rect()
        self.position = [x,y]
        self.speed=2
    
    def move_right(self):self.position[0]+=self.speed
    def move_left(self):self.position[0]-=self.speed
    def move_up(self):self.position[1]-=self.speed
    def move_down(self):self.position[1]+=self.speed
        
    def update(self):
       self.rect.topleft=self.position
       
    def get_image(self,x,y):
        image = pygame.Surface([24, 24])
        image.blit(self.sprite_sheet1, (0, 0), (x, y, 24, 24))
        image.blit(self.sprite_sheet2, (0, 0), (x, y, 24, 24))
        
        return image    
