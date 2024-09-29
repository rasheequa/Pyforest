import time
import pygame
import pytmx
import pyscroll
import pytmx.util_pygame
from src.sprite.mob import Mob
from src.sprite.player import Player
from src.strategie.ia import IA

class Game:
    
    def __init__(self):
        self.screen=pygame.display.set_mode((800,800))
        pygame.display.set_caption("Pyforest")
        
        tmx_data = pytmx.util_pygame.load_pygame("src/modele/pyforest.tmx")
        map_data=pyscroll.data.TiledMapData(tmx_data)
        map_layer=pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())

        map_layer.zoom=3

        player_position=tmx_data.get_object_by_name("mob")
        
        
        self.walls=[]
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x,obj.y, obj.width,obj.height))

        player_position=tmx_data.get_object_by_name("player")
        self.player=Player(player_position.x,player_position.y,self.walls)

        self.mob=Mob(player_position.x,player_position.y,self.walls)
        self.ia = IA(self.mob,self.player)

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)
        self.group.add(self.mob)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()

        if not (pressed[pygame.K_UP] or pressed[pygame.K_DOWN] or pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]):
            self.player.stop_moving()
        
        
    def update(self):

        self.group.update() 
        self.group.center(self.player.rect)
        self.ia.update()
      
       
    def run(self):
        clock=pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.mob.save_location()
            self.handle_input()
            self.update()
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 

            clock.tick(60)    

        pygame.quit()
    