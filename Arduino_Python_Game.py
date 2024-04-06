import pygame
import serial
import random

#### Make sure Arduino's Serial Monitor is NOT running ####

# Initialize Pygame and the Serial Port
pygame.init()
ser = serial.Serial('/dev/tty.usbmodem1101', 9600, timeout=0)  # Replace 'COM10' with your Arduino's serial port


# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpacerVibe")

# Load images
background_img = pygame.image.load('background_nologo.png').convert()
spaceship_img = pygame.image.load('spaceship.png').convert_alpha()
laser_img = pygame.image.load('laser.png').convert_alpha()
rock_img = pygame.image.load('rock.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
# Colors
BLACK = (0, 0, 0)

# Spaceship properties
# spaceship = pygame.Rect(WIDTH // 2, HEIGHT - 60, spaceship_img.get_width(), spaceship_img.get_height())
spaceship_speed = 15
spaceship_y_offset = -25

spaceship = pygame.Rect(WIDTH // 2 - spaceship_img.get_width() // 2,
                        HEIGHT - spaceship_img.get_height() - spaceship_y_offset,
                        spaceship_img.get_width(),
                        spaceship_img.get_height())

# Laser properties
lasers = []
laser_speed = 15

# Rock properties
rocks = []
rock_spawn_rate = 30  # Lower is more frequent
rock_fall_speed = 3

# FPS
FPS = 60
clock = pygame.time.Clock()

# Game loop
running = True
rock_timer = 0
laser_cooldown = 0
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Non-blocking read from the serial port
    data = ser.read(ser.inWaiting() or 1).decode('utf-8', errors='ignore')
    if data:
        try:
            joystick_x, button_pressed = (int(value) for value in data.strip().split(','))
            # Move spaceship based on joystick X value
            spaceship.x += joystick_x * spaceship_speed
            spaceship.x = max(0, min(WIDTH - spaceship.width, spaceship.x))
            # Shoot a laser if button is pressed and cooldown is over
            if button_pressed == 0 and laser_cooldown == 0:  # Assuming active-low button (pressed = 0)
                lasers.append(
                    pygame.Rect(spaceship.centerx - laser_img.get_width() // 2, spaceship.y, laser_img.get_width(),
                                laser_img.get_height()))
                laser_cooldown = 10  # Set cooldown period to prevent continuous firing
        except ValueError:
            pass

    # Decrease the cooldown
    if laser_cooldown > 0:
        laser_cooldown -= 1

    # Spawn rocks
    rock_timer += 1
    if rock_timer >= rock_spawn_rate:
        rock_timer = 0
        rock_size = random.randint(20, 50)
        rocks.append(pygame.Rect(random.randint(0, WIDTH - rock_size), 0, rock_size, rock_size))

    # Move rocks
    for rock in rocks[:]:
        rock.y += rock_fall_speed
        if rock.y > HEIGHT:
            rocks.remove(rock)

    # Move lasers
    for laser in lasers[:]:
        laser.y -= laser_speed
        if laser.y < 0:
            lasers.remove(laser)

    # Check for collisions
    for rock in rocks[:]:
        for laser in lasers[:]:
            if rock.colliderect(laser):
                rocks.remove(rock)
                lasers.remove(laser)
                break

    # Drawing
    screen.blit(background_img, (0, 0))
    #screen.fill(BLACK)
    for rock in rocks:
        screen.blit(rock_img, (rock.x, rock.y))
    for laser in lasers:
        screen.blit(laser_img, (laser.x, laser.y))
    screen.blit(spaceship_img, (spaceship.x, spaceship.y))


    pygame.display.flip()
    clock.tick(FPS)

ser.close()
pygame.quit()