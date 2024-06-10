import pygame
import pytmx
import pyscroll
import pytmx.util_pygame
from player import Player

class Game:
    
    def __init__(self):
        self.screen=pygame.display.set_mode((800,800))
        pygame.display.set_caption("Pyforest")
        
        tmx_data = pytmx.util_pygame.load_pygame('pyforest.tmx')
        map_data=pyscroll.data.TiledMapData(tmx_data)
        map_layer=pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())

        map_layer.zoom=3
        player_position=tmx_data.get_object_by_name("player")
        self.player=Player(player_position.x,player_position.y)
        
        
        self.walls=[]
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x,obj.y, obj.width,obj.height))
                
        
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=9)
        self.group.add(self.player)
        
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        else:
            self.player.stop_moving()
        
    def update(self):
        self.group.update() 
        self.group.center(self.player.rect)
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls)>-1:
                sprite.move_back()
          
       
    def run(self):
        clock=pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False    
            clock.tick(60)     
        pygame.quit()
    