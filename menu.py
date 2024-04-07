import pygame
import serial

import os

pygame.init()
pygame.font.init()
ser = serial.Serial('/dev/tty.usbmodem1101', 9600, timeout=0)  # Replace 'COM10' with your Arduino's serial port

WIDTH, HEIGHT = 800, 600
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

background_img = pygame.image.load('dino2.png').convert()

running = True

screen.blit(background_img, (0, 0))
font = pygame.font.Font(None,36)
text = font.render("Welcome to our game!", True, (255,255,255))
screen.blit(text,(200,60))
text = font.render("Left: Wander the flower fields", True, (255,255,255))
screen.blit(text,(200,120))
text = font.render("Top: Fight fires", True, (255,255,255))
screen.blit(text,(200,170))
text = font.render("Right: Catching Nemo", True, (255,255,255))
screen.blit(text,(200,220))
text = font.render("<3 Ashly & Amanda", True, (255,255,255))
screen.blit(text,(200,290))

while running:
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    data = ser.read(ser.inWaiting() or 1).decode('utf-8', errors='ignore')
    if data:
        try:
            joystick_x, joystick_y, up, right, down, left = (int(value) for value in data.strip().split(','))
            # Move Player based on joystick X value
            
            if up == 0:
                os.system("python3 fire.py")
            if left == 0:
                os.system("python3 flower.py")
            if right == 0:
                os.system("python3 ocean.py")
            

        except ValueError:
            pass

    

    
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
