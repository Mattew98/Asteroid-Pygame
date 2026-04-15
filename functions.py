# Asteroid pygame additional functions script
# University project
# Matthew Riddoch

# Import pygame
import pygame

# Import config file
import config as conf

def validate(entry,instance,bounds,name):
    # Type check
    errors = []
    if not isinstance(entry, instance):
        return True, "Error: ["+str(name)+"] of value ("+str(entry)+") is not of accepted types: ["+str(instance)+"]"
    
    # Bounds check
    error, error_message = False, "Valid"
    if bounds != (0,0):
        minimum = bounds[0]
        maximum = bounds[1]
        lesser_error = "Error: ["+str(name)+"] of value ("+str(entry)+") is less than accepted bound: ["+str(minimum)+"]"
        greater_error = "Error: ["+str(name)+"] of  value ("+str(entry)+") is greater than accepted bound: ["+str(maximum)+"]"
        if isinstance(entry,(tuple, list)): # Handle tuple entries for the colours validations
            for v in entry:
                if v < minimum:
                    error, error_message = True, lesser_error
                elif v > maximum:
                    error, error_message = True, greater_error
        else:
            if entry < bounds[0]:
                error, error_message = True, lesser_error
            elif entry > bounds[1]:
                error,error_message = True, greater_error
    return error, error_message

def write_text(screen, font, text, pos_x,pos_y,colour): # Writes a line of text on the screen
    text_render = font.render(text, False, colour)
    screen.blit(text_render, (pos_x,pos_y))

def controls_view(screen, status, font): # Grouped write_text() functions to keep code concise and avoid repetition every time the control guide is mentioned
    if status:
        write_text(screen, font, "Press ENTER/RETURN to Quit", 5, 680, conf.WHITE)
        write_text(screen, font, "W - Forward", 5, 695, conf.WHITE)
        write_text(screen, font, "A - Strafe Left", 5, 710, conf.WHITE)
        write_text(screen, font, "S - Backward", 5, 725, conf.WHITE)
        write_text(screen, font, "D - Strafe Right", 5, 740, conf.WHITE)
        write_text(screen, font, "Left Arrow - Rotate Left", 5, 755, conf.WHITE)
        write_text(screen, font, "Right Arrow - Rotate Right", 5, 770, conf.WHITE)
        write_text(screen, font, "Space - Fire", 5, 785, conf.WHITE)
    else:
        write_text(screen, font, "Press ESC to See Controls", 5, 785, conf.WHITE)

def cycle(array,current_index,direction): # Handles any cycle through an array (used for colour and difficulty picking from config options)
    if direction == "Left":
        if current_index > 0:
            return array[current_index - 1]
        else:
            return array[len(array) - 1] # Loop back to end
    elif direction == "Right":
        if current_index < len(array) - 1:
            return array[current_index + 1]
        else:
            return array[0] # Loop back to start

def collide(vertices1,vertices2): # Loops through object vertices to determine collision
    # One object needs to have a vertex within the bounds of another object
    less = False
    greater = False
    for point in vertices1:
        for point1 in vertices2:
            if point[0] < point1[0] and point[1] < point1[1]:
                less = True
            if point[0] > point1[0] and point[1] > point1[1]:
                greater = True
        if less and greater:
            return True # Collision condition satisfied
    return False



