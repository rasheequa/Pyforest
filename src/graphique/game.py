import pygame
import pytmx
import pyscroll
import pytmx.util_pygame
from src.sprite.mob import Mob
from src.sprite.player import Player
from src.strategie.ia import IA

class Game:
    # This class manages the main game logic, including the map, player, mobs, and AI

    def __init__(self):
        # Initialize the game window and set up the map, player, and mobs
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Pyforest")
        
        # Load the Tiled map and set up the map layer
        tmx_data = pytmx.util_pygame.load_pygame("src/modele/pyforest.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        map_layer.zoom = 3  # Zoom level for the map
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
    
        # Create collision walls from the map objects
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Set up the player at the starting position
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y, self.walls)
        self.group.add(self.player)
        
        # Set up mobs and their AI
        self.ia = []
        self.mobs = []
        for obj in tmx_data.objects:
            if obj.name == "mob":
                mob = Mob(obj.x, obj.y, self.walls)
                self.mobs.append(mob)
                self.group.add(mob)
                self.ia.append(IA(mob, self.player, tmx_data))

    def handle_input(self):
        # Handle player input for movement
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()

        # Stop the player if no movement keys are pressed
        if not (pressed[pygame.K_UP] or pressed[pygame.K_DOWN] or pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]):
            self.player.stop_moving()
        
    def update(self):
        # Update the game state, including the player, mobs, and AI
        self.group.update() 
        self.group.center(self.player.rect)  # Center the camera on the player
        for ia in self.ia:
            ia.update()

    def run(self):
        # Main game loop
        clock = pygame.time.Clock()
        running = True
        while running:
            self.handle_input()  # Handle player input
            self.update()  # Update the game state
            self.group.draw(self.screen)  # Draw the game objects
            pygame.display.flip()  # Update the display

            # Handle events like quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 

            clock.tick(60)  # Limit the game to 60 FPS

        pygame.quit()  # Quit the game when the loop ends
