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
        self.animation_timer_player = 0
        
        self.animation_speed_mob = 200  # Animation plus lente et stable pour le mouvement
        self.animation_speed_player = 110
        
        self.afk_animation_speed_mob = 400  # Encore plus lente pour idle
        self.afk_animation_speed_player = 300
        
        self.last_frame_time = 0  # Pour gérer la stabilité du framerate
        
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
            print(f"[ANIM DEBUG] Initialisation animation pour Mob {id(sprite)}")
            # Toujours commencer avec une direction valide et des animations chargées
            self.current_animation_direction = 'left'  # Direction par défaut
            
            # Initialiser tous les frames à None d'abord
            self.frames_left_mob = None
            self.frames_right_mob = None
            self.frames_afk_left_mob = None
            self.frames_afk_right_mob = None
            
            # Charger uniquement la direction initiale
            print(f"[ANIM DEBUG] Chargement initial animations gauche pour Mob {id(sprite)}")
            self.frames_left_mob = self.load_left_animation_images_mob()
            self.frames_afk_left_mob = self.load_afk_animation_images_mob('left')
            
            print(f"[ANIM DEBUG] État initial - Left: {self.frames_left_mob is not None}, AFKLeft: {self.frames_afk_left_mob is not None}, Right: {self.frames_right_mob is not None}, AFKRight: {self.frames_afk_right_mob is not None}") 
        
        

        
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
            # Use passed direction parameter
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
            images.append(self.get_image(5, frame))
        return images
    
    def load_afk_animation_images_mob(self,direction):
        images = []
        for frame in range(6):
            # Use the passed direction parameter rather than the sprite's current direction
            if direction == 'left':
                images.append(self.get_image(4, frame))
            elif direction == 'right':
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

    def change_animation_direction(self, new_direction):
        """Change la direction de l'animation en déchargeant l'ancienne direction"""
        print(f"[ANIM DEBUG] Mob {id(self.sprite)} - Changement direction: {self.current_animation_direction} -> {new_direction}")
        print(f"[ANIM DEBUG] État actuel - Left: {self.frames_left_mob is not None}, AFKLeft: {self.frames_afk_left_mob is not None}, Right: {self.frames_right_mob is not None}, AFKRight: {self.frames_afk_right_mob is not None}")
        
        if new_direction != self.current_animation_direction:
            # Décharger toutes les animations
            print(f"[ANIM DEBUG] Déchargement de toutes les animations pour {id(self.sprite)}")
            self.frames_left_mob = None
            self.frames_right_mob = None
            self.frames_afk_left_mob = None
            self.frames_afk_right_mob = None

            # Charger uniquement les nouvelles animations
            if new_direction == 'left':
                print(f"[ANIM DEBUG] Chargement animations gauche pour {id(self.sprite)}")
                self.frames_left_mob = self.load_left_animation_images_mob()
                self.frames_afk_left_mob = self.load_afk_animation_images_mob('left')
            else:
                print(f"[ANIM DEBUG] Chargement animations droite pour {id(self.sprite)}")
                self.frames_right_mob = self.load_right_animation_images_mob()
                self.frames_afk_right_mob = self.load_afk_animation_images_mob('right')

            self.current_animation_direction = new_direction
            self.current_frame_mob = 0  # Réinitialiser le frame counter
            
            print(f"[ANIM DEBUG] Nouvel état - Left: {self.frames_left_mob is not None}, AFKLeft: {self.frames_afk_left_mob is not None}, Right: {self.frames_right_mob is not None}, AFKRight: {self.frames_afk_right_mob is not None}")

    def animate_mob(self):
        now = pygame.time.get_ticks()
        
        # Limiter le taux de rafraîchissement global de l'animation
        if now - self.last_frame_time < 16:  # ~60 FPS max
            return
        self.last_frame_time = now

        # Determine actual mob direction from the underlying sprite (avoid desync)
        mob_dir = getattr(self.sprite, 'direction_mob', self.direction_mob)
        # Si la direction a changé, charger les nouvelles animations
        if mob_dir != self.current_animation_direction:
            print(f"[ANIM DEBUG] Mob {id(self.sprite)} - Direction change détectée: {self.current_animation_direction} -> {mob_dir}")
            self.change_animation_direction(mob_dir)

        # S'assurer qu'on a des animations valides
        move_frames = None
        idle_frames = None
        
        if self.current_animation_direction == 'left':
            move_frames = self.frames_left_mob
            idle_frames = self.frames_afk_left_mob
            if self.frames_right_mob is not None or self.frames_afk_right_mob is not None:
                print(f"[ANIM DEBUG] ERREUR: Mob {id(self.sprite)} a des animations droites chargées alors qu'il est tourné à gauche - correction automatique")
                # Force unload of opposite-side frames to maintain invariant
                self.frames_right_mob = None
                self.frames_afk_right_mob = None
        elif self.current_animation_direction == 'right':
            move_frames = self.frames_right_mob
            idle_frames = self.frames_afk_right_mob
            if self.frames_left_mob is not None or self.frames_afk_left_mob is not None:
                print(f"[ANIM DEBUG] ERREUR: Mob {id(self.sprite)} a des animations gauches chargées alors qu'il est tourné à droite - correction automatique")
                # Force unload of opposite-side frames to maintain invariant
                self.frames_left_mob = None
                self.frames_afk_left_mob = None
        else:
            # Fallback: ensure at least one set exists
            move_frames = self.frames_left_mob or self.frames_right_mob
            idle_frames = self.frames_afk_left_mob or self.frames_afk_right_mob

        # Animation en fonction de l'état de mouvement
        # Use mob_dir (actual mob direction) to drive animation selection
        if self.sprite.is_moving and move_frames:
            if now - self.animation_timer_mob > self.animation_speed_mob:
                self.animation_timer_mob = now
                self.image = move_frames[self.current_frame_mob % len(move_frames)]
                self.current_frame_mob = (self.current_frame_mob + 1) % len(move_frames)
        elif idle_frames:  # Animation idle
            if now - self.animation_timer_mob > self.afk_animation_speed_mob:
                self.animation_timer_mob = now
                self.image = idle_frames[self.current_frame_mob % len(idle_frames)]
                self.current_frame_mob = (self.current_frame_mob + 1) % len(idle_frames)

    def check_movement_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.sprite.is_moving = True
            self.afk_timer_player = pygame.time.get_ticks()  
        else:
            
            if pygame.time.get_ticks() - self.afk_timer_player > self.afk_delay_player:
                self.sprite.is_moving = False

    def check_movement_mob(self):
        # Pour les mobs IA, on regarde la velocity pour savoir s'ils bougent
        if hasattr(self.sprite, 'velocity'):
            if self.sprite.velocity.length_squared() > 0:
                self.sprite.is_moving = True
                self.afk_timer_mob = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.afk_timer_mob > self.afk_delay_mob:
                    self.sprite.is_moving = False
        else:
            # fallback clavier (jamais utilisé pour les mobs IA)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.sprite.is_moving = True
                self.afk_timer_mob = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.afk_timer_mob > self.afk_delay_mob:
                    self.sprite.is_moving = False