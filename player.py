import pygame, serial
from settings import *

ser = serial.Serial('/dev/tty.usbmodem1101', 9600, timeout=0)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('Player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
 
        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        
        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            self.direction.y = -1
        elif key[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if key[pygame.K_RIGHT]:
            self.direction.x = 1
        elif key[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        # data = ser.read(ser.inWaiting() or 1).decode('utf-8', errors='ignore')
        # print("DATA: ", data)
        # if data:
        #     try:
        #         joystick_x, button_pressed = (int(value) for value in data.strip().split(','))
        #         self.direction.x += joystick_x
        #     except ValueError:
        #         pass


    def move(self,speed):
        self.rect.center += self.direction * speed
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom


    def update(self):
        self.input()
        self.move(self.speed)