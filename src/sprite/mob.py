import pygame
import src.graphique.animation as animation
vector = pygame.math.Vector2

class Mob(animation.AnimateSprite):

    def __init__(self, x, y, walls):
        # Call the parent constructor to load the sprite and initialize
        super().__init__("blue mushroom sheet", None, self, x, y)
        
        # Create a smaller rectangle for more precise collision detection (the "feet")
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.walls = walls  # List of walls (obstacles) in the map
        
        # Physics constants
        self.HORIZONTAL_ACCELERATION = 0.1
        self.HORIZONTAL_FRICTION = 0.1

        # Speed and movement state
        self.speed_mob = 1.2 
        self.is_moving = False

        # Movement vectors
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.last_direction = vector(-1, 0)  # Default direction (left)

        # Save the spawn position
        self.spawn = self.position.copy()

    def set_acceleration(self, x, y):
        # Set the acceleration with a small factor
        self.acceleration = vector(x, y) * self.HORIZONTAL_ACCELERATION

    # Movement controls in four directions
    def move_right(self):
        self.acceleration.x = self.HORIZONTAL_ACCELERATION
        self.direction_mob = 'right'

    def move_left(self):
        self.acceleration.x = -self.HORIZONTAL_ACCELERATION
        self.direction_mob = 'left'

    def move_up(self):
        self.acceleration.y = -self.HORIZONTAL_ACCELERATION  

    def move_down(self):
        self.acceleration.y = self.HORIZONTAL_ACCELERATION  

    def stop_moving(self):
        # Stop all movement
        self.acceleration = vector(0, 0)  

    def get_image(self, row, frame):
        # Get a single frame from the sprite sheet
        image = pygame.Surface([24, 24], pygame.SRCALPHA)
        image.blit(self.sprite_sheet1, (0, 0), (frame * 16, row * 16, 16, 16))
        if hasattr(self, 'sprite_sheet2'):
            image.blit(self.sprite_sheet2, (0, 0), (frame * 24, row * 24, 24, 24))
        return image 

    def update(self):
        # Save the current position
        old_position = self.position.copy()
        # Predict the future position
        future_position = self.position + self.velocity

        # Check if the mob is moving
        min_velocity = 0.05
        self.is_moving = self.velocity.length() > min_velocity
        
        # Update the last direction when moving
        if self.is_moving:
            self.last_direction = self.velocity.normalize()
        
        # Update movement direction (left or right)
        if hasattr(self, 'last_direction'):
            if abs(self.last_direction.x) > abs(self.last_direction.y):
                self.direction_mob = 'right' if self.last_direction.x > 0 else 'left'

        # Move horizontally
        self.position.x = future_position.x
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        collided_x = self.check_collision(axis='x')

        # Move vertically
        self.position.y = future_position.y
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        collided_y = self.check_collision(axis='y')

        # Update the final position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        # Manage mob behavior and animation
        self.check_movement_mob()
        self.animate_mob()

    def check_collision(self, axis):
        # Check if the mob collides with any wall
        for obstacle in self.walls:
            if self.rect.colliderect(obstacle):
                if axis == 'x':
                    # Collision on the x-axis (horizontal)
                    if self.velocity.x > 0:  # Moving right
                        self.position.x = obstacle.left - self.rect.width  
                    elif self.velocity.x < 0:  # Moving left
                        self.position.x = obstacle.right 
                elif axis == 'y':
                    # Collision on the y-axis (vertical)
                    if self.velocity.y > 0:  # Moving down
                        self.position.y = obstacle.top - self.rect.height
                    elif self.velocity.y < 0:  # Moving up
                        self.position.y = obstacle.bottom 

                # Update position after collision
                self.rect.topleft = self.position
                self.feet.midbottom = self.rect.midbottom
                return True  # Collision happened
        return False  # No collision
