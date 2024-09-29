import time
import pygame

class AnimateSprite(pygame.sprite.Sprite):
    
    def __init__(self,  sprite_name1, sprite_name2, x, y):
        super().__init__()
        
        self.sprite_sheet1 = pygame.image.load(f'src/modele/characters/main character/{sprite_name1}.png')
        if sprite_name2 is not None:
            self.sprite_sheet2 = pygame.image.load(f'src/modele/characters/main character/{sprite_name2}.png')
        self.direction = 'right'
        self.is_moving = False
        
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed_player = 0.9
        self.speed_mob = 0.5
        self.current_frame = 0
        
        self.frames_left_player = self.load_left_animation_images_player()
        self.frames_right_player = self.load_right_animation_images_player()
        self.frames_afk_right_player = self.load_afk_animation_images_player('right')
        self.frames_afk_left_player = self.load_afk_animation_images_player('left') 

        self.frames_left_mob = self.load_left_animation_images_mob()
        self.frames_right_mob = self.load_right_animation_images_mob()
        self.frames_afk_right_mob = self.load_afk_animation_images_mob('right')
        self.frames_afk_left_mob = self.load_afk_animation_images_mob('left') 
        
        self.animation_timer = 0
        self.animation_speed_player = 110
        self.animation_speed_mob = 100
        self.afk_animation_speed_player = 300
        self.afk_animation_speed_mob = 250

        self.afk_timer = 0
        self.afk_delay = 2000

        
    def load_right_animation_images_player(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(2, frame))
        return images
    
    def load_left_animation_images_player(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(1, frame))      
        return images
        
    def load_afk_animation_images_player(self,direction):
        images = []
        for frame in range(2):
            if direction == 'left':
                images.append(self.get_image(0, frame))
            elif direction == 'right':
                images.append(self.get_image(0, frame+2))
        return images
    
    def load_right_animation_images_mob(self):
        images = []
        for frame in range(7):  
            images.append(self.get_image(1, frame))  
        return images
    
    def load_left_animation_images_mob(self):
        images = []
        for frame in range(7): 
            images.append(self.get_image(6, frame))
        return images
    
    def load_afk_animation_images_mob(self,direction):
        images = []
        for frame in range(6):
            if direction == 'left':
                images.append(self.get_image(5, frame))
            elif direction == 'right':
                images.append(self.get_image(0, frame))
        return images
    
    def animate_player(self):
        now = pygame.time.get_ticks()
        if self.is_moving:
            if now - self.animation_timer > self.animation_speed_player:
                self.animation_timer = now
                if self.direction == 'left':
                    self.image = self.frames_left_player[self.current_frame]
                elif self.direction == 'right':
                    self.image = self.frames_right_player[self.current_frame]
                
                self.current_frame += 1
                if self.current_frame >= len(self.frames_left_player):
                    self.current_frame = 0
                    
        else:
            if now - self.animation_timer > self.afk_animation_speed_player:
                self.animation_timer = now
                if self.direction == 'left':
                    self.image = self.frames_afk_left_player[self.current_frame % len(self.frames_afk_left_player)]
                else:
                    self.image = self.frames_afk_right_player[self.current_frame % len(self.frames_afk_right_player)]
                self.current_frame = (self.current_frame + 1) % len(self.frames_afk_left_player)

    def animate_mob(self):
        now = pygame.time.get_ticks()
        
       
        if self.is_moving:
            if now - self.animation_timer > self.animation_speed_mob:
                self.animation_timer = now
                if self.direction == 'left':
                    self.image = self.frames_left_mob[self.current_frame]
                elif self.direction == 'right':
                    self.image = self.frames_right_mob[self.current_frame]
                
                self.current_frame += 1
                if self.current_frame >= len(self.frames_left_mob):
                    self.current_frame = 0
                    
        else:
           
            if now - self.animation_timer > self.afk_animation_speed_mob:
                self.animation_timer = now
                if self.direction == 'left':
                    self.image = self.frames_afk_left_mob[self.current_frame % len(self.frames_afk_left_mob)]
                else:
                    self.image = self.frames_afk_right_mob[self.current_frame % len(self.frames_afk_right_mob)]
                self.current_frame = (self.current_frame + 1) % len(self.frames_afk_left_mob)

    def check_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.is_moving = True
            self.afk_timer = pygame.time.get_ticks()  
        else:
            
            if pygame.time.get_ticks() - self.afk_timer > self.afk_delay:
                self.is_moving = False