import pygame

class AnimateSprite(pygame.sprite.Sprite):
    
    def __init__(self,  sprite_name1, sprite_name2, x, y):
        super().__init__()
        self.sprite_sheet1 = pygame.image.load(f'Tiny Wonder Forest 1.0/characters/main character/{sprite_name1}.png')
        self.sprite_sheet2 = pygame.image.load(f'Tiny Wonder Forest 1.0/characters/main character/{sprite_name2}.png')
        
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 2

        self.current_frame = 0
        self.direction = 'right'
        self.is_moving = False
        
        self.frames_left = self.load_left_animation_images()
        self.frames_right = self.load_right_animation_images()
        self.frames_afk_right = self.load_afk_animation_images('right')
        self.frames_afk_left = self.load_afk_animation_images('left') 
        
        self.animation_timer = 0
        self.animation_speed = 115
        self.afk_animation_speed = 300

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
        
    def update(self):
        self.rect.topleft = self.position
        self.check_movement()
        self.animate()
       
    def get_image(self, row, frame):
        image = pygame.Surface([24, 24], pygame.SRCALPHA)
        image.blit(self.sprite_sheet1, (0, 0), (frame * 24, row * 24, 24, 24))
        image.blit(self.sprite_sheet2, (0, 0), (frame * 24, row * 24, 24, 24))
        return image  

    def load_left_animation_images(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(1, frame))
            
        return images
        
    def load_right_animation_images(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(2, frame))
        return images
    
    def load_left_animation_images(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(1, frame))
            
        return images
        
    def load_afk_animation_images(self,direction):
        images = []
        for frame in range(2):
            if direction == 'left':
                images.append(self.get_image(0, frame))
            elif direction == 'right':
                images.append(self.get_image(0, frame+2))
        return images

    def animate(self):
        now = pygame.time.get_ticks()
        if self.is_moving:
            if now - self.animation_timer > self.animation_speed:
                self.animation_timer = now
                if self.direction == 'left':
                    self.image = self.frames_left[self.current_frame]
                elif self.direction == 'right':
                    self.image = self.frames_right[self.current_frame]
                
                self.current_frame += 1
                if self.current_frame >= len(self.frames_left):
                    self.current_frame = 0
                    
        else:
            if now - self.animation_timer > self.afk_animation_speed:
                self.animation_timer = now
                if self.direction == 'left':
                    self.image = self.frames_afk_left[self.current_frame % len(self.frames_afk_left)]
                else:
                    self.image = self.frames_afk_right[self.current_frame % len(self.frames_afk_right)]
                self.current_frame = (self.current_frame + 1) % len(self.frames_afk_left)  
                
    def check_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.is_moving = True
        else:
            self.is_moving = False