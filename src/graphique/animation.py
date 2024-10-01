import time
import pygame

class AnimateSprite(pygame.sprite.Sprite):
    
    def __init__(self,  sprite_name1, sprite_name2, sprite, x, y):
        super().__init__()
        
        self.sprite_sheet1 = pygame.image.load(f'src/modele/characters/main character/{sprite_name1}.png')
        if sprite_name2 is not None:
            self.sprite_sheet2 = pygame.image.load(f'src/modele/characters/main character/{sprite_name2}.png')
        
        self.sprite=sprite
    
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()
        
        self.current_frame_mob = 0
        self.current_frame_player = 0

        self.animation_timer_mob = 0
        self.animation_timer_player= 0
        
        self.animation_speed_mob = 100
        self.animation_speed_player = 110
        
        self.afk_animation_speed_mob = 200
        self.afk_animation_speed_player = 300
        
        self.direction_player = 'right'
        self.direction_mob = 'left'

        self.afk_timer_mob = 0
        self.afk_delay_mob = 2000
        self.afk_timer_player = 0
        self.afk_delay_player = 2000

        
        if type(sprite).__name__ == "Player":
            self.frames_left_player = self.load_left_animation_images_player()
            self.frames_right_player = self.load_right_animation_images_player()
            self.frames_afk_right_player = self.load_afk_animation_images_player('right')
            self.frames_afk_left_player = self.load_afk_animation_images_player('left') 

        elif type(sprite).__name__ == "Mob":
            self.frames_left_mob = self.load_left_animation_images_mob()
            self.frames_right_mob = self.load_right_animation_images_mob()
            self.frames_afk_right_mob = self.load_afk_animation_images_mob('right')
            self.frames_afk_left_mob = self.load_afk_animation_images_mob('left') 
        
        

        
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
            if self.direction_player == 'left':
                images.append(self.get_image(0, frame))
            elif self.direction_player == 'right':
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
            images.append(self.get_image(5, frame))
        return images
    
    def load_afk_animation_images_mob(self,direction):
        images = []
        for frame in range(6):
            if self.direction_mob == 'left':
                images.append(self.get_image(4, frame))
            elif self.direction_mob == 'right':
                images.append(self.get_image(0, frame))
        return images
    
    def animate_player(self):
        now = pygame.time.get_ticks()
        if self.sprite.is_moving:
            if now - self.animation_timer_player > self.animation_speed_player:
                self.animation_timer_player = now
                if self.direction_player == 'left':
                    self.image = self.frames_left_player[self.current_frame_player]
                elif self.direction_player == 'right':
                    self.image = self.frames_right_player[self.current_frame_player]
                
                self.current_frame_player += 1
                if self.current_frame_player >= len(self.frames_left_player):
                    self.current_frame_player = 0
                    
        else:
            if now - self.animation_timer_player> self.afk_animation_speed_player:
                self.animation_timer_player = now
                if self.direction_player == 'left':
                    self.image = self.frames_afk_left_player[self.current_frame_player % len(self.frames_afk_left_player)]
                else:
                    self.image = self.frames_afk_right_player[self.current_frame_player % len(self.frames_afk_right_player)]
                self.current_frame_player = (self.current_frame_player + 1) % len(self.frames_afk_left_player)

    def animate_mob(self):
        now = pygame.time.get_ticks()
        if self.sprite.is_moving:
            if now - self.animation_timer_mob > self.animation_speed_mob:
                self.animation_timer_mob  = now
                if self.direction_mob == 'left':
                    self.image = self.frames_left_mob[self.current_frame_mob]
                elif self.direction_mob == 'right':
                    self.image = self.frames_right_mob[self.current_frame_mob]
                
                self.current_frame_mob += 1
                if self.current_frame_mob >= len(self.frames_left_mob):
                    self.current_frame_mob = 0
                    
        else:
            if now - self.animation_timer_mob  > self.afk_animation_speed_mob:
                self.animation_timer_mob  = now
                if self.direction_mob == 'left':
                    self.image = self.frames_afk_left_mob[self.current_frame_mob % len(self.frames_afk_left_mob)]
                else:
                    self.image = self.frames_afk_right_mob[self.current_frame_mob % len(self.frames_afk_right_mob)]
                self.current_frame_mob = (self.current_frame_mob + 1) % len(self.frames_afk_left_mob)

    def check_movement_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.sprite.is_moving = True
            self.afk_timer_player = pygame.time.get_ticks()  
        else:
            
            if pygame.time.get_ticks() - self.afk_timer_player > self.afk_delay_player:
                self.sprite.is_moving = False

    def check_movement_mob(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.sprite.is_moving = True
            self.afk_timer_mob = pygame.time.get_ticks()  
        else:
            
            if pygame.time.get_ticks() - self.afk_timer_mob > self.afk_delay_mob:
                self.sprite.is_moving = False