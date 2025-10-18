import pygame
import src.graphique.animation as animation

vector = pygame.math.Vector2

class Player(animation.AnimateSprite):
    
    def __init__(self, x, y, walls):
        # Call the parent constructor to load the sprite and set position
        super().__init__("walk and idle", "cat kigurumi walk and idle", self, x, y)
        
        # Create a smaller rectangle for more accurate collision (the "feet")
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.walls = walls  # List of obstacles

        # Physics constants for movement
        self.HORIZONTAL_ACCELERATION = 0.4
        self.HORIZONTAL_FRICTION = 0.2

        # Movement speed and state
        self.speed_player = 0.9
        self.is_moving = False

        # Vectors for movement
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        
    # Movement in four directions
    def move_right(self):
        self.acceleration.x = self.HORIZONTAL_ACCELERATION
        self.direction_player = 'right'
        self.is_moving = True

    def move_left(self):
        self.acceleration.x = -self.HORIZONTAL_ACCELERATION  
        self.direction_player = 'left'
        self.is_moving = True

    def move_up(self):
        self.acceleration.y = -self.HORIZONTAL_ACCELERATION
        self.is_moving = True

    def move_down(self):
        self.acceleration.y = self.HORIZONTAL_ACCELERATION
        self.is_moving = True
        
    def stop_moving(self):
        # Stop player movement
        self.is_moving = False
       
    def get_image(self, row, frame):
        # Get a frame from both sprite sheets
        image = pygame.Surface([24, 24], pygame.SRCALPHA)
        image.blit(self.sprite_sheet1, (0, 0), (frame * 24, row * 24, 24, 24))
        image.blit(self.sprite_sheet2, (0, 0), (frame * 24, row * 24, 24, 24))
        return image

    def update(self):
        # Update velocity with acceleration
        self.velocity += self.acceleration
        # Apply friction to reduce speed gradually
        self.velocity.x *= (1 - self.HORIZONTAL_FRICTION)
        self.velocity.y *= (1 - self.HORIZONTAL_FRICTION)

        # Predict the next position
        future_position = self.position + self.velocity

        # Move horizontally and check for collisions
        self.position.x = future_position.x
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.check_collision(axis='x')
    
        # Move vertically and check for collisions
        self.position.y = future_position.y
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.check_collision(axis='y')

        # Reset acceleration each frame
        self.acceleration = vector(0, 0)
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

        # Handle movement logic and animation
        self.check_movement_player()
        self.animate_player()
        
    def check_collision(self, axis):
        # Check if the player touches a wall
        for obstacle in self.walls:
            if self.rect.colliderect(obstacle):
                if axis == 'x':
                    # Collision on x-axis (horizontal)
                    if self.velocity.x > 0:  # Moving right
                        self.position.x = obstacle.left - self.rect.width  
                    elif self.velocity.x < 0:  # Moving left
                        self.position.x = obstacle.right 
                elif axis == 'y':
                    # Collision on y-axis (vertical)
                    if self.velocity.y > 0:  # Moving down
                        self.position.y = obstacle.top - self.rect.height
                    elif self.velocity.y < 0:  # Moving up
                        self.position.y = obstacle.bottom 

                # Update position after collision
                self.rect.topleft = self.position
                self.feet.midbottom = self.rect.midbottom
                return True  # Collision happened
        return False  # No collision
