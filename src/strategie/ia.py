import math
import pygame

class IA:
    def __init__(self, mob, player):
        self.mob = mob
        self.player = player
        self.metre = 16
        self.pixel = 16
        self.radius = self.pixel * self.metre
        self.min_distance = 50

        # Intervalle de mise à jour
        self.move_update_interval = 10  
        self.last_move_time = pygame.time.get_ticks()

        # Ajout d'une vitesse de base pour le mob
        self.max_speed = 1.5  # Vitesse maximale
        self.min_speed = 0.5  # Vitesse minimale pour éviter les saccades à proximité
        
    def update(self):
        current_time = pygame.time.get_ticks()

        # Calculer la distance entre le mob et le joueur
        dx = self.player.position[0] - self.mob.position[0]
        dy = self.player.position[1] - self.mob.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Vérifier le temps depuis la dernière mise à jour
        if current_time - self.last_move_time > self.move_update_interval:
            self.last_move_time = current_time

            # Si la distance est dans la zone d'attraction mais en dehors de la distance minimale
            if self.min_distance < distance < self.radius:

                # Calcul de la vitesse proportionnelle à la distance (ralenti à proximité)
                speed = max(self.min_speed, min(self.max_speed, distance / self.radius * self.max_speed))

                # Normaliser le vecteur de direction
                direction_x = dx / distance if distance != 0 else 0
                direction_y = dy / distance if distance != 0 else 0

                # Déplacer le mob progressivement dans la direction du joueur
                self.mob.position[0] += direction_x * speed
                self.mob.position[1] += direction_y * speed

                # Déterminer la direction pour l'animation
                if direction_x > 0:
                    self.mob.move_right()
                else:
                    self.mob.move_left()

                if direction_y > 0:
                    self.mob.move_down()
                else:
                    self.mob.move_up()
            else:
                self.mob.stop_moving()
