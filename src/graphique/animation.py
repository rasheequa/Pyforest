import time
import pygame

class AnimateSprite(pygame.sprite.Sprite):
    # This class handles sprite animations for the game
    # It manages animations for both the player and mobs

    def __init__(self, sprite_name1, sprite_name2, sprite, x, y):
        super().__init__()
        # Initialize the sprite with its images and animation settings

        self.sprite_sheet1 = pygame.image.load(f'src/modele/characters/main character/{sprite_name1}.png')
        if sprite_name2 is not None:
            self.sprite_sheet2 = pygame.image.load(f'src/modele/characters/main character/{sprite_name2}.png')

        self.sprite = sprite

        self.image = self.get_image(0, 0)  # Load the first image of the sprite
        self.rect = self.image.get_rect()  # Get the rectangle for positioning

        # Animation settings for mobs and players
        self.current_frame_mob = 0
        self.current_frame_player = 0

        self.animation_timer_mob = 0
        self.animation_timer_player = 0

        self.animation_speed_mob = 200  # Speed of mob animations
        self.animation_speed_player = 110  # Speed of player animations

        self.afk_animation_speed_mob = 400  # Speed of idle animations for mobs
        self.afk_animation_speed_player = 300  # Speed of idle animations for players

        self.last_frame_time = 0  # Time of the last frame update

        self.direction_player = 'right'  # Default direction for the player
        self.direction_mob = 'left'  # Default direction for mobs

        self.afk_timer_mob = 0
        self.afk_delay_mob = 2000  # Delay before mobs go idle
        self.afk_timer_player = 0
        self.afk_delay_player = 2000  # Delay before the player goes idle

        # Load animations based on the type of sprite (Player or Mob)
        if type(sprite).__name__ == "Player":
            self.frames_left_player = self.load_left_animation_images_player()
            self.frames_right_player = self.load_right_animation_images_player()
            self.frames_afk_right_player = self.load_afk_animation_images_player('right')
            self.frames_afk_left_player = self.load_afk_animation_images_player('left')

        elif type(sprite).__name__ == "Mob":
            self.current_animation_direction = 'left'  # Default direction for mob animations

            # Initialize mob animation frames
            self.frames_left_mob = None
            self.frames_right_mob = None
            self.frames_afk_left_mob = None
            self.frames_afk_right_mob = None

            self.frames_left_mob = self.load_left_animation_images_mob()
            self.frames_afk_left_mob = self.load_afk_animation_images_mob('left')

    # Load animation frames for the player's right movement
    def load_right_animation_images_player(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(2, frame))
        return images

    # Load animation frames for the player's left movement
    def load_left_animation_images_player(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(1, frame))
        return images

    # Load idle animation frames for the player.
    def load_afk_animation_images_player(self, direction):
        images = []
        for frame in range(2):
            if direction == 'left':
                images.append(self.get_image(0, frame))
            elif direction == 'right':
                images.append(self.get_image(0, frame + 2))
        return images

    # Load animation frames for the mob's right movement
    def load_right_animation_images_mob(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(1, frame))
        return images

    # Load animation frames for the mob's left movement
    def load_left_animation_images_mob(self):
        images = []
        for frame in range(7):
            images.append(self.get_image(5, frame))
        return images

    # Load idle animation frames for the mob
    def load_afk_animation_images_mob(self, direction):
        images = []
        for frame in range(6):
            if direction == 'left':
                images.append(self.get_image(4, frame))
            elif direction == 'right':
                images.append(self.get_image(0, frame))
        return images

    # Animate the player based on movement or idle state
    def animate_player(self):
        now = pygame.time.get_ticks()
        if self.sprite.is_moving:
            # Animate movement
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
            # Animate idle state
            if now - self.animation_timer_player > self.afk_animation_speed_player:
                self.animation_timer_player = now
                if self.direction_player == 'left':
                    self.image = self.frames_afk_left_player[self.current_frame_player % len(self.frames_afk_left_player)]
                else:
                    self.image = self.frames_afk_right_player[self.current_frame_player % len(self.frames_afk_right_player)]
                self.current_frame_player = (self.current_frame_player + 1) % len(self.frames_afk_left_player)

    # Change the animation direction for the mob
    def change_animation_direction(self, new_direction):
        if new_direction != self.current_animation_direction:
            # Clear old animation frames
            self.frames_left_mob = None
            self.frames_right_mob = None
            self.frames_afk_left_mob = None
            self.frames_afk_right_mob = None

            # Load new animation frames based on the direction
            if new_direction == 'left':
                self.frames_left_mob = self.load_left_animation_images_mob()
                self.frames_afk_left_mob = self.load_afk_animation_images_mob('left')
            else:
                self.frames_right_mob = self.load_right_animation_images_mob()
                self.frames_afk_right_mob = self.load_afk_animation_images_mob('right')

            self.current_animation_direction = new_direction
            self.current_frame_mob = 0

    # Animate the mob based on movement or idle state
    def animate_mob(self):
        now = pygame.time.get_ticks()

        if now - self.last_frame_time < 16:  # Limit frame updates to 60 FPS
            return
        self.last_frame_time = now

        mob_dir = getattr(self.sprite, 'direction_mob', self.direction_mob)

        if mob_dir != self.current_animation_direction:
            self.change_animation_direction(mob_dir)

        move_frames = None
        idle_frames = None

        if self.current_animation_direction == 'left':
            move_frames = self.frames_left_mob
            idle_frames = self.frames_afk_left_mob
        elif self.current_animation_direction == 'right':
            move_frames = self.frames_right_mob
            idle_frames = self.frames_afk_right_mob
        else:
            move_frames = self.frames_left_mob or self.frames_right_mob
            idle_frames = self.frames_afk_left_mob or self.frames_afk_right_mob

        if self.sprite.is_moving and move_frames:
            # Animate movement
            if now - self.animation_timer_mob > self.animation_speed_mob:
                self.animation_timer_mob = now
                self.image = move_frames[self.current_frame_mob % len(move_frames)]
                self.current_frame_mob = (self.current_frame_mob + 1) % len(move_frames)
        elif idle_frames:
            # Animate idle state
            if now - self.animation_timer_mob > self.afk_animation_speed_mob:
                self.animation_timer_mob = now
                self.image = idle_frames[self.current_frame_mob % len(idle_frames)]
                self.current_frame_mob = (self.current_frame_mob + 1) % len(idle_frames)

    # Check if the player is moving and update the state
    def check_movement_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.sprite.is_moving = True
            self.afk_timer_player = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - self.afk_timer_player > self.afk_delay_player:
                self.sprite.is_moving = False

    # Check if the mob is moving and update the state
    def check_movement_mob(self):
        if hasattr(self.sprite, 'velocity'):
            if self.sprite.velocity.length_squared() > 0:
                self.sprite.is_moving = True
                self.afk_timer_mob = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.afk_timer_mob > self.afk_delay_mob:
                    self.sprite.is_moving = False
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.sprite.is_moving = True
                self.afk_timer_mob = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.afk_timer_mob > self.afk_delay_mob:
                    self.sprite.is_moving = False