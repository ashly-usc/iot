import pygame
import serial
import random
import os

#### Make sure Arduino's Serial Monitor is NOT running ####

# Initialize Pygame and the Serial Port
pygame.init()
ser = serial.Serial('/dev/tty.usbmodem1101', 9600, timeout=0)  # Replace 'COM10' with your Arduino's serial port

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flowers")

# Load images
background_img = pygame.image.load('higrass.png').convert()
Player_img = pygame.image.load('Player.png').convert_alpha()
flower_img = pygame.image.load('Grass_3.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
flower_img = pygame.transform.scale(flower_img, (32, 32))

# Player properties
Player_speed = 15
Player_y_offset = -25

Player = pygame.Rect(WIDTH // 2 - Player_img.get_width() // 2,
                        HEIGHT - Player_img.get_height() - Player_y_offset,
                        Player_img.get_width(),
                        Player_img.get_height())

# flower properties
flowers = []

# FPS
FPS = 60
clock = pygame.time.Clock()

# Game loop
running = True
flowers.append(pygame.Rect(random.randint(0, WIDTH - 32), random.randint(0, HEIGHT - 32), 32, 32))
flowers.append(pygame.Rect(random.randint(0, WIDTH - 32), random.randint(0, HEIGHT - 32), 32, 32))
flowers.append(pygame.Rect(random.randint(0, WIDTH - 32), random.randint(0, HEIGHT - 32), 32, 32))
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Non-blocking read from the serial port
    data = ser.read(ser.inWaiting() or 1).decode('utf-8', errors='ignore')
    if data:
        try:
            joystick_x, joystick_y, up, right, down, left = (int(value) for value in data.strip().split(','))
            # Move Player based on joystick X value
            Player.x += joystick_x * Player_speed
            Player.x = max(0, min(WIDTH - Player.width, Player.x))
            Player.y += joystick_y * Player_speed
            Player.y = max(0, min(HEIGHT - Player.height, Player.y))
            if up == 0:
                os.system("python3 fire.py")
            if down == 0:
                os.system("python3 menu.py")
            if right == 0:
                os.system("python3 ocean.py")
        except ValueError:
            pass

    # Check for collisions
    for flower in flowers[:]:
            if flower.colliderect(Player):
                flowers.remove(flower)
                flowers.append(pygame.Rect(random.randint(0, WIDTH - 32), random.randint(0, HEIGHT - 32), 32, 32))
                break

    # Drawing
    screen.blit(background_img, (0, 0))
    for flower in flowers:
        screen.blit(flower_img, (flower.x, flower.y))
    screen.blit(Player_img, (Player.x, Player.y))

    pygame.display.flip()
    clock.tick(FPS)

ser.close()
pygame.quit()
