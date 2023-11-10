import pygame
import sys
from scenario import Background
import pygame.freetype


# font colors 
#D6AC2B
#CF843F
#B96933


class PygameMenu:
    def __init__(self, screen, menu_options):
        self.screen = screen
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 600
        self.menu_options = menu_options
        self.selected_option = 0
        self.font = pygame.font.Font("font/8-BIT_WONDER.TTF", 25)
        self.font_title = pygame.font.Font("font/8-BIT_WONDER.TTF", 50)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255,255,0)
        self.BLACK = (0, 0, 0)
        self.ORANGE = (255,181,2)
        self.BROWN = (128,90,0)
        self.FPS = 60
        self.scroll = 0
        self.background = Background(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)


    def draw_menu(self):
        self.screen.fill(self.WHITE)
        self.background.draw_bg(self.scroll)
        self.background.draw_ground(self.scroll)




        title_text = self.font_title.render("START GAME", True, self.ORANGE)
        title_text_shadow = self.font_title.render("START GAME", True, self.BROWN)
        self.screen.blit(title_text_shadow, (300, 228))
        self.screen.blit(title_text, (300, 220))


        for i, option in enumerate(self.menu_options):
            text = self.font.render(option, True, self.ORANGE)
            text_shadow = self.font.render(option, True, self.BROWN)
            text_rect_shadow = text.get_rect(center=(545, 334  + i * 35))
            text_rect = text.get_rect(center=(545, 330  + i * 35))
            self.screen.blit(text_shadow, text_rect_shadow)
            self.screen.blit(text, text_rect)

            if i == self.selected_option:
                arrow_x = 380  # Define the x-coordinate for the arrow based on your layout
                arrow_y = 320 + i * 35  
                
                triangle_points = [(arrow_x, arrow_y), (arrow_x + 20, arrow_y + 10), (arrow_x, arrow_y + 20)]
                pygame.draw.polygon(self.screen, self.BLACK, triangle_points, 0)


    def run(self):
        menu_active = True

        while menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    if event.key == pygame.K_LEFT:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    if event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Start
                            menu_active = False
                            # Call a function to start the game
                        elif self.selected_option == 1:  # Level
                            # Call a function to go to the level selection
                            pass
                        elif self.selected_option == 2:  # Options
                            # Call a function to open the options menu
                            pass

            self.draw_menu()
            pygame.display.flip()
            pygame.time.Clock().tick(self.FPS)

