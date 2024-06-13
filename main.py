import pygame
from src.graphique.game import Game
from src.graphique.animation import AnimateSprite
from src.sprite.player import Player


if __name__ == '__main__':
    pygame.init()
    game=Game()
    game.run()
    
    
    
    