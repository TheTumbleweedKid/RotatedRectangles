# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 15:27:35 2022

@author: Tumbl
"""

import pygame
from numpy import radians

from rotated_rectangle import RotatedRectangle

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Bahnschrift', 30)

modes = ("point", "circle", "rect")
mode = 0
mode_text = font.render(
    "Mode: " + modes[mode] + " (press 'm' to change)",
    False,
    (0, 0, 0))
# Model objects that moved with the mouse, collide with the static rectangle.
# [0] = point location/centre of circle
# [1] = radius of circle
# [2] = RotatedRectangle object
models = ([0, 0], 15, RotatedRectangle(0, 0, 50, 50))

# Create the static rectangle (that collisions will be tested against).
rect = RotatedRectangle(250, 150, 75, 35)
# Position/rotate it according to your heart's desire.
rect.set_rotation(radians(-75))
rect.set_position(158, 340)

def colliding_rect():
    # Utility function (to avoid code duplication). Returns whether the
    # active model is colliding with the static rectangle.
    if mode == 0:
        return rect.contains_point(models[0])   
    if mode == 1:
        return rect.overlaps_circle(models[0], models[1])
    else:
        return rect.overlaps_rot_rect(models[2])

bg_colour = (155, 155, 155)

done = False

while not done:
    # Update model locations:
    # Point/circle centre
    models[0][0] = pygame.mouse.get_pos()[0]
    models[0][1] = pygame.mouse.get_pos()[1]
    # Rectangle
    models[2].set_position(
        pygame.mouse.get_pos()[0],
        pygame.mouse.get_pos()[1])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # Quit the program
            done = True
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if colliding_rect():
                # Green background - collision detected!
                bg_colour = (155, 255, 155)
            else:
                # Red background - no collision detected!
                bg_colour = (255, 155, 155)
        elif event.type == pygame.KEYUP and event.key == pygame.K_m:
                mode += 1
                
                if mode >= len(modes):
                    mode = 0
                
                mode_text = font.render(
                    "Mode: " + modes[mode] + " (press 'm' to change)",
                    False,
                    (0, 0, 0))
    
    # Update graphics.
    window.fill(bg_colour)
    # Draw mode text.
    window.blit(mode_text, (250, 5))
    # Draw mouse-coordinates.
    window.blit(
        font.render(
            "X: " + str(round(pygame.mouse.get_pos()[0])),
            False,
            (0, 0, 0)),
        (550, 45))
    window.blit(
        font.render(
            "Y: " + str(round(pygame.mouse.get_pos()[1])),
            False,
            (0, 0, 0)),
        (550, 75))
    # Draw static RotatedRectangle.
    pygame.draw.lines(
        window,
        (0, 0, 0),
        True,
        rect.points)
    # Draw the model object (if there is one)
    if mode == 1:
        pygame.draw.circle(
            window,
            (255, 255, 100),
            models[0],
            models[1],
            width=1)
    elif mode == 2:
        pygame.draw.lines(
            window,
            (255, 255, 100),
            True,
            models[2].points)
    
    pygame.display.flip()
    clock.tick(60)
            
pygame.quit()
quit()
