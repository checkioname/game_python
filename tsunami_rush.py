import pygame
from hero import Player
from Menu import PygameMenu
from game import Game
from gameOver import GameOver
from agent import AIPlayer


pygame.init()

# create game window
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tsunami Rush")

test_font = pygame.font.Font("font/VT323-Regular.ttf", 25)

# Create instances of Game, PygameMenu, and GameOver
game = Game(0,0)
menu = PygameMenu(screen, ["1 PLAYER", "2 PLAYERS", "EXIT"])
game_over = GameOver(screen, 0, 0)  # Initialize with score and high score

# Game state variables
in_menu = True
in_game_one_player = False
in_game_two_player = False

# Timer variables
return_to_menu_timer = 0
return_to_menu_duration = 2  # Set the duration in seconds


# musica
# Musica do jogo
pygame.mixer.music.load("sounds/8-bit-game-music-122259.mp3")
pygame.mixer.music.set_volume(0.5)
# Start playing the background music (use -1 to loop indefinitely)

# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if in_menu:
        menu.run()
        if menu.selected_option == 0:
            pygame.mixer.music.play(-1)
            in_menu = False
            in_game_one_player = True
        elif menu.selected_option == 1:
            pygame.mixer.music.play(-1)
            in_menu = False
            in_game_two_player = True
        elif menu.selected_option == 2:
            run = False

    elif in_game_one_player:
        game.agent = None
        done, score, hi_score = game.step()
        if done == 0:
            pygame.mixer.music.stop()
            if game.score > game.hi_score:
                game.hi_score = game.score
            game.reset()
            for i in range(100):
                #atualiza a tela e mostra game over por alguns segundos
                pygame.display.flip()
                game_over.draw_game_over_screen(score,hi_score)

            in_menu = True
            in_game_one_player = False

    elif in_game_two_player:
        game.agent = AIPlayer(400,520,'sprites/ai_player', 0.05, 0, state_size=7, action_size=2)
        while True:
            done, score, hi_score = game.step()
            if done == 0:
                if game.score > game.hi_score:
                    game.hi_score = game.score
                pygame.mixer.music.stop()
                game.agent = AIPlayer(400,520,'sprites/ai_player', 0.05, 0, state_size=7, action_size=2)
                game.reset()
                break
        for i in range(100):
            #atualiza a tela e mostra game over por alguns segundos
            pygame.display.flip()
            game_over.draw_game_over_screen(score,hi_score)
            game_over.high_score = game.hi_score

        in_menu = True
        in_game_two_player = False
        in_game_one_player = False




pygame.quit()
