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
pygame.display.set_caption("Ocean")
fish_size = 32

# Load images
background_img = pygame.image.load('ocean.png').convert()
Player_img = pygame.image.load('Player.png').convert_alpha()
nemo_img = pygame.image.load('nemo.png').convert_alpha()
dory_img = pygame.image.load('dory.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
nemo_img = pygame.transform.scale(nemo_img, (fish_size, fish_size))
dory_img = pygame.transform.scale(dory_img, (fish_size, fish_size))

# Player properties
Player_speed = 15
Player_y_offset = -25

Player = pygame.Rect(WIDTH // 2 - Player_img.get_width() // 2,
                        HEIGHT - Player_img.get_height() - Player_y_offset,
                        Player_img.get_width(),
                        Player_img.get_height())

# fish properties
fish = []
fish_spawn_rate = 30  # Lower is more frequent
fish_fall_speed = 3

# FPS
FPS = 60
clock = pygame.time.Clock()

# Game loop
running = True
fish_timer = 0
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
            if left == 0:
                os.system("python3 flower.py")
            if down == 0:
                os.system("python3 menu.py")
        except ValueError:
            pass
    # Spawn fish
    fish_timer += 1
    if fish_timer >= fish_spawn_rate:
        fish_timer = 0
        fish.append(pygame.Rect((WIDTH - fish_size), random.randint(0, HEIGHT - fish_size), fish_size, fish_size))

    # Move fishs
    for f in fish[:]:
        f.x -= fish_fall_speed
        if f.x < 0:
            fish.remove(f)
    
    # Check for collisions
    for f in fish[:]:
            if f.colliderect(Player):
                fish.remove(f)
                break

    # Drawing
    screen.blit(background_img, (0, 0))
    i = 0
    for f in fish:
        if i%2 == 0:
            screen.blit(nemo_img, (f.x, f.y))
        else:
            screen.blit(dory_img, (f.x, f.y))
        i = i+1

    screen.blit(Player_img, (Player.x, Player.y))

    pygame.display.flip()
    clock.tick(FPS)

ser.close()
pygame.quit()
