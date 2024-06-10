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

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        map_layer.zoom=3
        player_position=tmx_data.get_object_by_name("player")
        self.player=Player(player_position.x,player_position.y)
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
        self.handle_input()
        self.group.center(self.player.rect)
          
       
    def run(self):
        clock=pygame.time.Clock()
        running = True
        while running:
            self.update()
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False    
            clock.tick(60)     
        pygame.quit()
    