import pygame

class Background:
    def __init__(self, screen_width, screen_height,screen):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.screen = screen
        self.bg_images = []
        self.bg_width = 0
        self.ground_image = pygame.image.load(
            "Forest_tileset/Tiles/floor.jpeg"
        ).convert_alpha()
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height()

        for i in range(1, 5):
            bg_image = pygame.image.load(f"Forest_tileset/BG/{i}.png").convert_alpha()
            self.bg_images.append(bg_image)
        self.bg_width = self.bg_images[0].get_width()


    def draw_bg(self, scroll):
        for x in range(2000):
            speed = 1
            for i in self.bg_images:
                self.screen.blit(i, ((x * self.bg_width) - scroll * speed, 0))
                speed += 0.2

    def draw_ground(self, scroll):
        for x in range(2000):
            self.screen.blit(
                self.ground_image,
                ((x * self.ground_width) - scroll * 1.0, self.SCREEN_HEIGHT - self.ground_height),
            )
            x += 1

    #def draw_platform(self,scroll)


    