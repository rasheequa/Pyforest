import pygame
import animation
class Player(animation.AnimateSprite):
    
    def __init__(self,x,y):
        super().__init__("walk and idle","cat kigurumi walk and idle",x,y)

          
