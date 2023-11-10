import os
import pygame
from random import randint


class Sprites(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, path, current_sprite, run_speed):
        super().__init__()
        self.is_animating = False
        self.inc = current_sprite
        self.run_speed = run_speed

        # Carregamento de spriteslist
        dir = os.listdir(path)
        dir.sort()
        self.sprites = [pygame.image.load(path + '/' + i) for i in dir if 'png' in i]

        self.current_sprite = 0.0
        self.image = self.sprites[int(self.current_sprite)]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.mask = pygame.mask.from_surface(self.image)

        self.is_jumping = False
        self.jump_vel = 5
        self.jump_sprites = self.sprites

    def animate(self):
        self.is_animating = True

    def update(self):
        self.current_sprite += self.inc
        self.rect.x -= self.run_speed
        if self.rect.x <= -10:
            self.rect.x = randint(1000, 3050)

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            self.is_animating = False
        self.image = self.sprites[int(self.current_sprite)]
    
    def jump(self):
        if self.is_jumping:
            self.rect.y -= self.jump_vel * 1.5
            self.jump_vel -= 0.16

        if self.jump_vel < -5:
            self.rect.y = 500
            self.is_jumping = False
            self.jump_vel = 5