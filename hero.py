import os
import pygame
from random import randint
from sprites import Sprites

class Player(Sprites):

    def __init__(self, pos_x, pos_y, player_path, current_sprite, run_speed):
        super().__init__(pos_x, pos_y, player_path, current_sprite, run_speed)
        self.is_jumping = False
        self.jump_vel = 8.5
        self.jump_sprites = []
        self.jump_sprites.append(pygame.image.load('sprites/hero/jump/image_5.png'))
        self.jump_sprites.append(pygame.image.load('sprites/hero/jump/image_6.png'))

    def jump(self):
        if self.is_jumping:
            self.image = self.jump_sprites[0]
            self.rect.y -= self.jump_vel * 2.5
            self.jump_vel -= 0.45

        if self.jump_vel <= 0:
            self.image = self.jump_sprites[1]

        if self.jump_vel < -8.5:
            self.rect.y = 500
            self.is_jumping = False
            self.jump_vel = 8.5
