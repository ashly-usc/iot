import pygame
import serial
import random
import os

#### Make sure Arduino's Serial Monitor is NOT running ####

# Initialize Pygame and the Serial Port
pygame.init()
pygame.font.init()
ser = serial.Serial('/dev/tty.usbmodem1101', 9600, timeout=0)  # Replace 'COM10' with your Arduino's serial port

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fire!")
fire_size = 50

# Load images
background_img = pygame.image.load('floor.png').convert()
Player_img = pygame.image.load('Player.png').convert_alpha()
fire_img = pygame.image.load('twinflame.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
fire_img = pygame.transform.scale(fire_img, (fire_size, fire_size))

# Player properties
Player_speed = 15
Player_y_offset = -25

Player = pygame.Rect(WIDTH // 2 - Player_img.get_width() // 2,
                        HEIGHT - Player_img.get_height() - Player_y_offset,
                        Player_img.get_width(),
                        Player_img.get_height())

# fire properties
fires = []
fire_spawn_rate = 30  # Lower is more frequent

# FPS
FPS = 60
clock = pygame.time.Clock()

# Game loop
running = True
fire_timer = 0
fires.append(pygame.Rect(random.randint(0, WIDTH - fire_size), random.randint(200, HEIGHT - fire_size), fire_size, fire_size))
fires.append(pygame.Rect(random.randint(0, WIDTH - fire_size), random.randint(200, HEIGHT - fire_size), fire_size, fire_size))
fires.append(pygame.Rect(random.randint(0, WIDTH - fire_size), random.randint(200, HEIGHT - fire_size), fire_size, fire_size))
while running:
    # Drawing
    screen.blit(background_img, (0, 0))
    for fire in fires:
        screen.blit(fire_img, (fire.x, fire.y))
    screen.blit(Player_img, (Player.x, Player.y))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if len(fires) >= 10:
        font = pygame.font.Font(None, 60)
        text = font.render('You Lose', True, (255,255,255),(25,25,25))
        screen.blit(text,(300,250))
        text = font.render('* womp womp *', True, (255,255,255),(25,25,25))
        screen.blit(text,(230,300))
        pygame.display.update
        Player_speed = 0

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
            if down == 0:
                os.system("python3 menu.py")
            if left == 0:
                os.system("python3 flower.py")
            if right == 0:
                os.system("python3 ocean.py")
        except ValueError:
            pass
    
    fire_timer += 1
    if fire_timer >= fire_spawn_rate:
        fire_timer = 0
        fires.append(pygame.Rect(random.randint(0, WIDTH - fire_size), random.randint(200, HEIGHT - fire_size), fire_size, fire_size))
    
    # Check for collisions
    for fire in fires[:]:
            if fire.colliderect(Player):
                fires.remove(fire)
                break

    pygame.display.flip()
    clock.tick(FPS)

ser.close()
pygame.quit()
