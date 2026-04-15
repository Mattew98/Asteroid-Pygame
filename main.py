# Asteroid pygame main script
# University project
# Matthew Riddoch

# Library imports
import pygame
import random
import math

# File imports
import classes as gclass
import config as conf
import functions as func

# Initialize Pygame
pygame.init()

# Set up the game screen
screen = pygame.display.set_mode((conf.WIDTH, conf.HEIGHT))
pygame.display.set_caption("Asteroid Game")

# Fonts
font = pygame.font.SysFont("Arial", 24)
titlefont = pygame.font.SysFont("Arial", 50)
subtitlefont = pygame.font.SysFont("Arial",36)

# Global variables
clock = pygame.time.Clock()
playing = True
error = False
error_message = ""
error_messages = []

# Debug dictionary
debugs = {
    "Screen Width ":[conf.WIDTH, int, (1,7680)], # The largest made screen size, checking the actual local resolution would require more libraries
    "Screen Height":[conf.HEIGHT, int, (1,7680)],
    "FPS":[conf.FPS, int, (1,math.inf)], # The FPS has to be a positive integer
    "Shield Size":[conf.SHIELD_SIZE, int, (conf.SHIP_SIZE+1,math.inf)], # The shield size must be greater than the ship's size
    "Minimum Asteroid Radius":[conf.ASTEROID_RADIUS_MIN, int, (10,math.inf)], # The asteroid size minimum cannot be larger than the maximum
    "Maximum Asteroid Radius":[conf.ASTEROID_RADIUS_MAX, int, (conf.ASTEROID_RADIUS_MIN+1,math.inf)],
    "Minimum Asteroid Speed":[conf.ASTEROID_SPEED_MIN, int, (1,conf.ASTEROID_SPEED_MAX-1)], # The asteroid speed minimum cannot be larger than the maximum
    "Maximum Asteroid Speed":[conf.ASTEROID_SPEED_MAX, int, (conf.ASTEROID_SPEED_MIN+1,math.inf)],
    "Asteroid Split Size Threshold":[conf.ASTEROID_SPLIT_SIZE, int, (11,conf.ASTEROID_RADIUS_MAX-1)], # Split size has to be between the smallest possible size and the maximum
    "Starting Number of Asteroids":[conf.ASTEROID_START, int, (1,math.inf)],
    "Number of asteroid vertices":[conf.ASTEROID_VERTICES, int, (3,math.inf)], # Has to be at least 3 vertices to make a 2D shape
    "Bullet Radius":[conf.BULLET_RADIUS, (int,float), (1,math.inf)],
    "Bullet Speed":[conf.BULLET_SPEED, (int,float), (0,math.inf)],
    "Ship Size":[conf.SHIP_SIZE, (int,float), (1,conf.SHIELD_SIZE-1)], # Ship size cannot be larger than shield size
    "Score Increment":[conf.SCORE_INCREMENT, int, (1,math.inf)],
    "Difficulty Types":[conf.DIFFICULTY_TYPES, list, (0,0)],
    "Asteroid Number Added Each Round":[conf.ASTEROID_NUMBER, dict, (0,0)],
    "Damage Multiplier":[conf.DAMAGE_MULTIPLIER, dict, (0,0)],
    "Ship Health":[conf.SHIP_HEALTH, dict, (0,0)],
    "Shield Health":[conf.SHIELD_HEALTH, dict, (0,0)],
    "Eigengrau":[conf.EIGENGRAU, tuple, (0,0)],
    "List of colours":[conf.COLOURS, list, (0,0)]
}

for debug in debugs: # Loops through debug dictionary to validate values
    dictionary = debugs[debug]
    value = dictionary[0]
    instance = dictionary[1]
    bounds = dictionary[2]
    debug_error, message = func.validate(value,instance,bounds,debug)
    if instance == dict and not error: # If the value is a dictionary, validate all the values inside that dictionary
        if debug == "List of colours": # Colours is the only dictionary with different bounds and contains tuples
            for colour in value:
                debug_error, message = func.validate(value[colour],tuple,(0,255),"One of the colours")
        elif debug == "Damage Multiplier":
            for entry in value:
                debug_error, message = func.validate(value[entry],(int,float),(0,math.inf),debug+": "+entry)
        else:
            for entry in value:
                debug_error,message = func.validate(value[entry],(int),(1,math.inf),debug+": "+entry)
    if debug_error:
        error = True
        error_message = message
        error_messages.append(message)
        print(error_message)
   
# Screen loop, encloses all loops in case of replay
while playing and not error:

    # Game variables
    ready = False
    running = True
    end_screen = False
    shooting = False
    view_controls = True

    pygame.mouse.set_visible(False) # Hide the cursor

    # Scores
    score = 0
    rounds = 1

    # Object containers
    debris=[]
    bullets = []
    asteroids = []

    # Debounces Dict
    debounces = {"damage":0,"controls":0}

    # Starter Menu Loop
    while not ready and not error:
        screen.fill(conf.EIGENGRAU)
        # Write text for the menu
        func.write_text(screen, titlefont, "Project Asteroid Game", 600, 375, conf.WHITE)
        func.write_text(screen, font, "Press Space to Start", 600, 425, conf.WHITE)
        func.controls_view(screen, view_controls, font) # Display control guide
        func.write_text(screen, font, "Q < Ship Colour > E", 600, 500, conf.SHIP_COLOUR)
        func.write_text(screen, font, "A < Asteroid Colour > D", 600, 525, conf.ASTEROID_COLOUR)
        func.write_text(screen, font, "Z < Bullet Colour > C", 600, 550, conf.BULLET_COLOUR)
        func.write_text(screen, subtitlefont, "- < "+conf.DIFFICULTY+" > =", 600, 600, conf.WHITE)
        # Get the current selected colours and difficulties' relative index in their arrays
        ship_index = conf.COLOURS.index(conf.SHIP_COLOUR)
        asteroidindex = conf.COLOURS.index(conf.ASTEROID_COLOUR)
        bullet_index = conf.COLOURS.index(conf.BULLET_COLOUR)
        difficulty_index = conf.DIFFICULTY_TYPES.index(conf.DIFFICULTY)
        #Update the display each loop
        pygame.display.update()
        clock.tick(conf.FPS)
        # Controls for starter menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ready = True
                if event.key == pygame.K_q:
                    conf.SHIP_COLOUR = func.cycle(conf.COLOURS,ship_index,"Left") # Cycle left in colour array using ship colour
                elif event.key == pygame.K_e:
                    conf.SHIP_COLOUR = func.cycle(conf.COLOURS,ship_index,"Right") # Cycle right in colour array using ship colour
                if event.key == pygame.K_a:
                    conf.ASTEROID_COLOUR = func.cycle(conf.COLOURS,asteroidindex,"Left") # Cycle left in colour array using asteroid colour
                elif event.key == pygame.K_d:
                    conf.ASTEROID_COLOUR = func.cycle(conf.COLOURS,asteroidindex,"Right") # Cycle right in colour array using asteroid colour
                if event.key == pygame.K_z:
                    conf.BULLET_COLOUR = func.cycle(conf.COLOURS,bullet_index,"Left") # Cycle left in colour array using bullet colour
                elif event.key == pygame.K_c:
                    conf.BULLET_COLOUR = func.cycle(conf.COLOURS,bullet_index,"Right") # Cycle right in colour array using bullet colour
                if event.key == pygame.K_MINUS:
                    conf.DIFFICULTY = func.cycle(conf.DIFFICULTY_TYPES,difficulty_index,"Left") # Cycle left in difficulty array
                elif event.key == pygame.K_EQUALS:
                    conf.DIFFICULTY = func.cycle(conf.DIFFICULTY_TYPES,difficulty_index,"Right") # Cycle right in difficulty array
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    ready = True
                    running = False
                    playing = False

    view_controls = False # Reset control view for game start

    # Initialize the ship and asteroids
    ship = gclass.Ship(conf.WIDTH // 2, conf.HEIGHT // 2, 0, conf.SHIP_SPEED)
    debris.append(ship)
    for _ in range(conf.ASTEROID_START):
        # Create asteroids at only the top or bottom of the screen so there aren't immediate collisions with the ship
        new_asteroid = gclass.Asteroid(random.randint(0, conf.WIDTH), random.randint(0, 1)*800,
                            random.randint(conf.ASTEROID_RADIUS_MIN, conf.ASTEROID_RADIUS_MAX), random.randint(0, 360),
                            random.randint(conf.ASTEROID_SPEED_MIN, conf.ASTEROID_SPEED_MAX))
        asteroids.append(new_asteroid)
        debris.append(new_asteroid)

    while running and not error:
        screen.fill(conf.EIGENGRAU) # Background screen color
        for deb in debounces: # One loop for all debounces
            error, error_message = func.validate(debounces[deb], int,(0,math.inf), "Debounce: ["+deb+"]")
           
            if debounces[deb] > 0:
                debounces[deb] -= 1

        # Loop check for health and shield values
        # Initially set to zero so no negative values on display if either go below zero
        health = 0
        shield = 0
        if ship.health >= 0:
            # Use rounded integers for clear display
            health = round(ship.health)
            shield = round(ship.shield_health)
        else:
            # If the player dies, remove all objects
            for v in debris:
                debris.remove(v)
                if v in asteroids:
                    asteroids.remove(v)
                if v in bullets:
                    bullets.remove(v)
            # Quit game loop and start end screen
            end_screen = True
            running = False

        # Write updated stats display in top-left corner
        func.write_text(screen, font, "Score: "+str(score), 5, 5, conf.WHITE)
        func.write_text(screen, font, "Round: "+str(rounds), 5, 20, conf.WHITE)
        func.write_text(screen, font, "Health: "+str(health), 5, 35, (255-(255*health/conf.SHIP_HEALTH[conf.DIFFICULTY]),255*health/conf.SHIP_HEALTH[conf.DIFFICULTY],0))
        func.write_text(screen, font, "Shield: "+str(shield), 5, 50, (50,50,150))
        func.controls_view(screen, view_controls, font) # Update control guide

        # Check if all asteroids have been destroyed to start the next round
        if len(asteroids) == 0:
            rounds += 1
            ship.shield_health = conf.SHIELD_HEALTH[conf.DIFFICULTY] # Reset shield for new round
            for _ in range(conf.ASTEROID_START + (conf.ASTEROID_NUMBER[conf.DIFFICULTY] * (rounds-1))): # Change number of asteroids with difficulty
                new_asteroid = gclass.Asteroid(random.randint(0, conf.WIDTH), random.randint(0, 1)*800,
                                    random.randint(conf.ASTEROID_RADIUS_MIN, conf.ASTEROID_RADIUS_MAX), random.randint(0, 360),
                                    random.randint(conf.ASTEROID_SPEED_MIN, conf.ASTEROID_SPEED_MAX))
                asteroids.append(new_asteroid)
                debris.append(new_asteroid)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False     #This stops the inf loop (closing the game) - extremely important, do not alter unless you know what you are doing

        # Handle ship controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            end_screen = True # Enable end screen
            running = False # Quit game
        if keys[pygame.K_ESCAPE]:
            if debounces["controls"] == 0:
                view_controls = not view_controls # Show control guide
                debounces["controls"] = 15 # Reset debounce
        if keys[pygame.K_w]:
            ship.move_towards(ship.x,ship.y-conf.SHIP_SPEED) # Move forward
        if keys[pygame.K_a]:
            ship.move_towards(ship.x-conf.SHIP_SPEED,ship.y) # Move left
        if keys[pygame.K_s]:
            ship.move_towards(ship.x,ship.y+conf.SHIP_SPEED) # Move backward
        if keys[pygame.K_d]:
            ship.move_towards(ship.x+conf.SHIP_SPEED,ship.y) # Move right
        if keys[pygame.K_LEFT]:
            ship.rotate(-conf.SHIP_SPEED)  # Rotate counterclockwise
        if keys[pygame.K_RIGHT]:
            ship.rotate(conf.SHIP_SPEED)  # Rotate clockwise    
        if keys[pygame.K_SPACE]:
            if not shooting:
                new_bullet = gclass.Bullet(ship.x, ship.y, ship.angle)
                bullets.append(new_bullet)
                debris.append(new_bullet)
                shooting = True
        if not keys[pygame.K_SPACE]:
            shooting = False # Boolean debounce for shooting

        # Move and draw bullets
        for bullet in bullets:
            bullet.move()
            bullet.draw()
            if bullet.x < (0 - bullet.size) or bullet.x > (conf.WIDTH + bullet.size) or bullet.y < (0 - bullet.size) or bullet.y > (conf.HEIGHT + bullet.size): # Remove bullet if off-screen
                bullets.remove(bullet)
                debris.remove(bullet)

        # Move and draw asteroids
        asteroids_to_remove = []  # List of asteroids to remove
        new_asteroids = []  # List of new asteroids to add

        # Check for collisions
        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw()
            # Check for collisions
            for collider in debris:
                if math.sqrt((asteroid.x - collider.x)**2+(asteroid.y - collider.y)**2) < asteroid.size*1.2 + collider.size*1.2 and collider != asteroid: # Use the size for an in initial circular hitbox
                    colliding = func.collide(collider.vertices,asteroid.vertices) # Refine hitbox using object's vertices
                    if colliding == True:
                        error, error_message = func.validate(collider.type, str,(0,0), "class.type attribute")                      
                        if collider.type == "Bullet":
                            # Mark the asteroid for removal and split it into new asteroids
                            asteroids_to_remove.append(asteroid)
                            bullets.remove(collider)
                            debris.remove(collider)
                            asteroid_split = asteroid.split()
                            if asteroid_split != 0:
                                new_asteroids.extend(asteroid_split)
                            else:
                                score += conf.SCORE_INCREMENT # Add to player score
                        if collider.type == "Asteroid":
                            # Save values here so the second deflect does not use the asteroid's updated values
                            new_angle, new_speed, new_x, new_y, new_size = asteroid.angle, asteroid.speed, asteroid.x, asteroid.y, asteroid.size
                            # Run deflect functions
                            asteroid.deflect(collider.angle,collider.speed, collider.x, collider.y, collider.size)
                            collider.deflect(new_angle,new_speed,new_x,new_y,new_size)
                        if collider.type == "Ship":
                            # Damage the players
                            if debounces["damage"] == 0:
                                collider.damage(asteroid.size)
                                debounces["damage"] = 60
                            # Apply new angle for deflected asteroid
                            ang = math.degrees(math.tan((ship.y-asteroid.y)/(ship.x-asteroid.x))) % 360
                            if ang < 0: ang = ang % 360 + 360 # Get angle between 0 and 360 to make it clearer for debugging
                            # Validate the angle by relative position, if incorrect add 180 degrees to fix
                            if asteroid.x > ship.x and asteroid.y > ship.y:
                                if not (ang <= 90 and ang > 0): ang += 180
                            if asteroid.x < ship.x and asteroid.y > ship.y:
                                if not (ang <= 180 and ang > 90): ang += 180
                            if asteroid.x < ship.x and asteroid.y < ship.y:
                                if not (ang <= 270 and ang > 180): ang += 180
                            if asteroid.x > ship.x and asteroid.y < ship.y:
                                if not (ang <= 360 and ang > 270): ang += 180
                            asteroid.deflect(ang, conf.SHIP_SPEED, ship.x, ship.y, ship.size+asteroid.size) # Deflect the asteroid


        # After the loop, remove destroyed asteroids and add new ones from splitting
        for asteroid in asteroids_to_remove:
            if asteroid in asteroids:
                asteroids.remove(asteroid)
                debris.remove(asteroid)
        asteroids.extend(new_asteroids)
        debris.extend(new_asteroids)

        # Update the ship's display
        ship.draw()
        # Update the display
        pygame.display.update()
        # Limit the frame rate
        clock.tick(conf.FPS)

    while end_screen: # End Screen with game results
        screen.fill(conf.EIGENGRAU)
        func.write_text(screen, titlefont, "Game Over", 600, 350, conf.WHITE)
        func.write_text(screen, font, "Score: "+str(score), 600, 400, conf.WHITE)
        func.write_text(screen, font, "Rounds Survived: "+str(rounds), 600, 450, conf.WHITE)
        func.write_text(screen, font, "Diffculty: "+conf.DIFFICULTY, 600, 500, conf.WHITE)
        func.write_text(screen, font, "Press W to Try Again", 600, 600, conf.WHITE)
        func.write_text(screen, font, "Press Enter/Return to Quit", 600, 650, conf.WHITE)
        pygame.display.update()
        clock.tick(conf.FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                ready = False
                end_screen = False # Quit end screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False
                playing = False # Quit entire loop
                end_screen = False # Quit end screen

if error: # Load an error screen
    while error:
        screen.fill(conf.EIGENGRAU)
        func.write_text(screen, font,error_message,400,400,conf.WHITE)
        func.write_text(screen, font,str(len(error_messages))+" total errors",400,450,conf.WHITE)
        func.write_text(screen, font,"Press Enter/Return to Quit",400,500,conf.WHITE)
        pygame.display.update()
        clock.tick(conf.FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.quit()
                error = False
                playing = False
else:
    pygame.quit() # Quit pygame if no error and all loops ended