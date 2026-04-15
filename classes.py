# Asteroid pygame classes script
# University project
# Matthew Riddoch

# Library imports
import pygame
import math
import random

# File imports
import config as conf
import functions as func

# Screen reference
screen = pygame.display.set_mode((conf.WIDTH, conf.HEIGHT))

# Ship class
class Ship:
    def __init__(self, x, y, angle, speed): # Ship has x,y coordinates, angle, speed and size
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.size = conf.SHIP_SIZE
        self.shield_size = conf.SHIELD_SIZE
        self.type = "Ship" # Used for class check in collision condition
        self.health = conf.SHIP_HEALTH[conf.DIFFICULTY]
        self.shield_health = conf.SHIELD_HEALTH[conf.DIFFICULTY]
        self.vertices = [] # To be updated depending on shield health

    def move_towards(self, target_x, target_y): # Function that moves the ship towards target
        dx, dy = target_x - self.x, target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / distance * self.speed, dy / distance * self.speed
        self.x += dx
        self.y += dy

    def rotate(self, direction): # Function that rotates the ship (changes its angle)
        self.angle += direction

    def damage(self,size): # Handles ship health and shield health
        self.shield_health -= conf.DAMAGE_MULTIPLIER[conf.DIFFICULTY]*size
        if self.shield_health <= 0:
            self.health += self.shield_health
            self.shield_health = 0

    def draw(self): # Update ship display
        ship_points = [
            (self.x + math.cos(math.radians(self.angle)) * self.size, 
             self.y + math.sin(math.radians(self.angle)) * self.size),  # Top of ship
            (self.x + math.cos(math.radians(self.angle + 150)) * self.size, 
             self.y + math.sin(math.radians(self.angle + 150)) * self.size),  # Bottom left
            (self.x + math.cos(math.radians(self.angle + 180)) * self.size, 
             self.y + math.sin(math.radians(self.angle + 180)) * self.size),   # Back of ship
            (self.x + math.cos(math.radians(self.angle + 210)) * self.size, 
             self.y + math.sin(math.radians(self.angle + 210)) * self.size)   # Bottom right
        ]
        shield_points = [
            (self.x + math.cos(math.radians(self.angle)) * (self.shield_size+10), 
             self.y + math.sin(math.radians(self.angle)) * (self.shield_size+10)), # Tip of shield
            (self.x + math.cos(math.radians(self.angle + 15)) * self.shield_size, 
             self.y + math.sin(math.radians(self.angle + 15)) * self.shield_size), # Top left
            (self.x + math.cos(math.radians(self.angle + 135)) * self.shield_size, 
             self.y + math.sin(math.radians(self.angle + 135)) * self.shield_size),
            (self.x + math.cos(math.radians(self.angle + 165)) * self.shield_size, 
             self.y + math.sin(math.radians(self.angle + 165)) * self.shield_size),  # Bottom left
            (self.x + math.cos(math.radians(self.angle + 180)) * self.shield_size, 
             self.y + math.sin(math.radians(self.angle + 180)) * self.shield_size),   # Back of shield
            (self.x + math.cos(math.radians(self.angle + 195)) * self.shield_size, 
             self.y + math.sin(math.radians(self.angle + 195)) * self.shield_size),
            (self.x + math.cos(math.radians(self.angle + 225)) * self.shield_size, 
             self.y + math.sin(math.radians(self.angle + 225)) * self.shield_size),   # Bottom right
            (self.x + math.cos(math.radians(self.angle + 345)) * self.shield_size, 
             self.y + math.sin(math.radians(self.angle + 345)) * self.shield_size),  # Top right
        ]
        if self.shield_health > 0:
            pygame.draw.polygon(screen, (50,50,100), shield_points)
            self.vertices = shield_points
        else:
            self.vertices = ship_points
        pygame.draw.polygon(screen, conf.SHIP_COLOUR, ship_points)

# Bullet class
class Bullet:
    def __init__(self, x, y, angle):   # Bullet has x,y coordinates and an angle
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = conf.BULLET_SPEED
        self.dx = math.cos(math.radians(angle)) * self.speed
        self.dy = math.sin(math.radians(angle)) * self.speed
        self.size = conf.BULLET_RADIUS
        self.type = "Bullet"

    def move(self):    # Move bullet
        self.x += self.dx
        self.y += self.dy

    def draw(self): # Update bullet display
        self.vertices = [
            (self.x + math.cos(math.radians(self.angle)) * self.size*1.2, 
             self.y + math.sin(math.radians(self.angle)) * self.size*1.2), # Bullet tip
            (self.x + math.cos(math.radians(self.angle+30)) * self.size, 
             self.y + math.sin(math.radians(self.angle+30)) * self.size), # Bullet right shoulder
            (self.x + math.cos(math.radians(self.angle+120)) * self.size, 
             self.y + math.sin(math.radians(self.angle+120)) * self.size), # Bullet bottom right
            (self.x + math.cos(math.radians(self.angle+240)) * self.size, 
             self.y + math.sin(math.radians(self.angle+240)) * self.size), # Bullet bottom left
            (self.x + math.cos(math.radians(self.angle+330)) * self.size, 
             self.y + math.sin(math.radians(self.angle+330)) * self.size) # Bullet left shoulder
        ]
        pygame.draw.polygon(screen, conf.BULLET_COLOUR, self.vertices)

# Asteroid class
class Asteroid:
    def __init__(self, x, y, size, angle, speed):  # Asteroid has x,y coordinates, angle, angle and speed
        self.x = x
        self.y = y
        self.size = size
        self.angle = angle
        self.speed = speed
        self.dx = math.cos(math.radians(angle)) * self.speed
        self.dy = math.sin(math.radians(angle)) * self.speed
        self.type = "Asteroid"
        self.vertices = []
        self.tilt = random.randint(0,360) # So the asteroid rotation does not look the same each time, i.e. they don't all have a vertex at 0 radians
        self.vertex_sizes = [] # Create a predetermined array for each asteroid so the vertex lengths are not updated with every draw() function like the other classes
        for i in range(conf.ASTEROID_VERTICES+2*(self.size//10)): # Increase number of vertices with asteroid size for better visuals
            self.vertex_sizes.append(random.randint(round(0.8*self.size),round(self.size)))

    def move(self): # Handles movement and loops asteroids position to the other end if the asteroid disappears off screen completely
        self.old_x = self.x
        self.old_y = self.y
        self.x += self.dx
        self.y += self.dy
        # Wrap around the screen edges
        if self.x < (0 - self.size):
            self.x = conf.WIDTH + self.size
        elif self.x > (conf.WIDTH + self.size):
            self.x = 0 - self.size
        if self.y < (0 - self.size):
            self.y = conf.HEIGHT + self.size
        elif self.y > (conf.HEIGHT + self.size):
            self.y = 0 - self.size

    def draw(self): #Update asteroid display
        self.vertices.clear()
        for i in range(len(self.vertex_sizes)):
            self.vertices.append(((self.x + math.cos(math.radians(self.tilt + (360*i/len(self.vertex_sizes))))*self.vertex_sizes[i]),
            self.y + math.sin(math.radians(self.tilt + (360*i/len(self.vertex_sizes))))*self.vertex_sizes[i]))
        pygame.draw.polygon(screen, conf.ASTEROID_COLOUR, self.vertices)

    def deflect(self, other_angle, other_speed, other_x, other_y, other_size): # Handles collisions by causing a static and then elastic collision
        # Static Collision
        dist = math.sqrt((self.x-other_x)**2 + (self.y-other_y)**2)
        ideal_dist = self.size + other_size
        self.x += (self.x-other_x)*((ideal_dist-dist)/dist)/2
        self.y += (self.y-other_y)*((ideal_dist-dist)/dist)/2
        # Elastic Collisions
        ratio = self.size/(other_size+self.size)
        self.angle = other_angle
        self.speed = (other_speed+self.speed) * ratio
        self.dx = math.cos(math.radians(other_angle))*other_speed
        self.dy = math.sin(math.radians(other_angle))*other_speed

    def split(self):    #Split asteroid when hit and return two new, smaller asteroids
        if self.size > conf.ASTEROID_SPLIT_SIZE:
            new_size1 = random.randint(10,round(self.size/2)) # Set a minimum size of 10 so the asteroids are still visible (hardcoded as this should not be changed)
            new_size2 = self.size - new_size1 # Conserve the total size so new_size1 + new_size2 = original asteroid's size for reliable dimensions
            new_speed1 = random.randint(conf.ASTEROID_SPEED_MIN, conf.ASTEROID_SPEED_MAX)
            new_speed2 = conf.ASTEROID_SPEED_MAX + 1 - new_speed1 # New speeds, both in the range same range, with a total equal to the maximum speed, to keep the speeds reasonable
            new_angle1 = self.angle + random.randint(-45,45)
            new_angle2 = self.angle + random.randint(-45,45)
            return [
                Asteroid(self.x +1+ new_size1, self.y +1+ new_size1, new_size1, self.angle + new_angle1, new_speed1), # Add 1 to position values to separate them
                Asteroid(self.x -1- new_size2, self.y -1- new_size2, new_size2, self.angle + new_angle2, new_speed2)# Subtract 1 from position values to separate them
            ]
        return 0 # If the asteroid is too small to split