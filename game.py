import pygame
import sys
from random import randint
from scenario import Background
from hero import Player
from gameOver import GameOver
from time import sleep
from agent import AIPlayer
from gameOver import GameOver
from sprites import Sprites
import torch
import os
from torch.utils.tensorboard import SummaryWriter

class Game:
    def __init__(self, score, hi_score):
        self.test_font = pygame.font.Font("font/8-BIT_WONDER.TTF", 25)
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 600
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.ORANGE = (255,181,2)
        self.BROWN = (128,90,0)

        #Grupo de sprites do jogador
        self.moving_sprites = pygame.sprite.Group()
        self.player = Player(300, 500, 'sprites/hero', 0.05,0)
        self.moving_sprites.add(self.player)

        #Grupo de sprites da onda
        self.moving_wave = pygame.sprite.Group()
        self.wave = Sprites(-9, 320, 'sprites/WAVE', 0.05, 0)
        self.moving_wave.add(self.wave)

        #Grupo de sprites da moeda
        self.moving_coin = pygame.sprite.Group()
        self.coin = Sprites(randint(600, 1000), 500, 'sprites/GoldCoinSprite', 0.15, 5)
        self.moving_coin.add(self.coin)

        #Grupo de sprites do tubarao
        self.moving_shark = pygame.sprite.Group()
        self.shark = Sprites(1500, 430, 'sprites/shark', 0.15, 10)
        self.moving_shark.add(self.shark)


        self.moving_ai = pygame.sprite.Group()
        self.agent = AIPlayer(400,520,'sprites/ai_player', 0.05, 0, state_size=7, action_size=2)
        self.moving_ai.add(self.agent)


        self.moving_bomb = pygame.sprite.Group()
        self.bomb = Sprites(randint(10000, 30000), 500, 'sprites/bomb', 0.0, 5)
        self.moving_bomb.add(self.bomb)
        # Pontuação do jogo
        self.score = score  
        self.hi_score = hi_score
        
        self.scroll = 0
        self.background = Background(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen)

        self.two_players = True
        
    

    ####################################
    #           METODOS DO JOGO        #
    ####################################

    def draw_game_elements(self):
        self.moving_sprites.draw(self.screen)
        self.moving_sprites.update()
        self.moving_coin.draw(self.screen)
        self.moving_coin.update()
        self.moving_wave.draw(self.screen)
        self.moving_wave.update()
        self.moving_shark.draw(self.screen)
        self.moving_shark.update()
        if self.two_players:
            self.moving_ai.draw(self.screen)
            self.moving_ai.update()
        
        self.moving_bomb.draw(self.screen)
        self.moving_bomb.update()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.is_jumping = True

    def get_state(self):
        #altura do obstaculo
        #comprimento do obstaculo
        #distancia do obstaculo
        #altura da ia
        #comprimento da ia
        #distancia da moeda
        #altura da moeda
        #comprimento da moeda
        #esta pulando
        distancia_max = 1000

        distance_normalized = (self.agent.rect[0] - self.shark.rect[0]) / distancia_max

        is_jumping = None
        if self.agent.is_jumping:
            is_jumping = 1
        else:
            is_jumping = 0
        return [self.shark.rect[0], (self.agent.rect[0] - self.shark.rect[0]), self.agent.rect[0], is_jumping]



    def step(self):
        self.scroll += 4
        self.background.draw_bg(self.scroll)
        self.background.draw_ground(self.scroll)
        self.draw_game_elements()
        self.handle_events()
        self.render_scores()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.is_jumping = True

        if self.player.is_jumping:
            self.player.jump()

            
        if self.score > 300:
            self.shark.run_speed = 12
        if self.score > 500: 
            self.shark.run_speed = 14
        if self.score >800:
            self.shark.run_speed = 16

        self.score += 0.02  # Increment the score over time
        action = None 


        if self.two_players and self.agent is not None:
            distancia_max = 1000
            distancia_normalizada = (self.agent.rect[0] - self.shark.rect[0]) / distancia_max

            is_jumping = None
            if self.agent.is_jumping:
                is_jumping = 1
            else:
                is_jumping = 0
            
            state = [self.shark.rect[0], (self.agent.rect[0] - self.shark.rect[0]), self.agent.rect[0], is_jumping]
            action = self.agent.select_action(state)
            self.action = action
            print(f'VALOR DA ACAO {action}')

        if action == 1:
            self.agent.is_jumping = True
            
        if self.two_players and self.agent is not None:
            if  self.agent.is_jumping:
                self.agent.jump()
                action = 0


        
        self.bomb.is_jumping = True
        self.bomb.jump()


        # Change bomb sprite
        if self.bomb.rect.x <= 650:
            self.bomb.inc = 0.12
        else:
            self.bomb.current_sprite = 0.0


        # Check if the player collides with the coin
        if self.two_players and self.agent is not None:
            if self.agent.rect.colliderect(self.coin) or self.coin.rect.colliderect(self.agent):
                self.score += 10  # Increase the score when the player collects a coin
                # Move the coin to a new position
                hit = pygame.mixer.Sound("sounds/Pickup Coin3.wav")
                hit.play()
                self.coin.rect.x = randint(1000, 3000)  
                self.coin.rect.y = randint(350,500)
        
        if self.player.rect.colliderect(self.coin):
            self.score += 10  # Increase the score when the player collects a coin
            # Move the coin to a new position
            hit = pygame.mixer.Sound("sounds/Pickup Coin3.wav")
            hit.play()
            self.coin.rect.x = randint(1000, 3000)  
            self.coin.rect.y = randint(350,500)


        if self.two_players and self.agent is not None:
            if self.agent.rect.colliderect(self.bomb):
                self.two_players = False
        
        


        # Check for collisions with the shark and update the score accordingly
        if self.two_players and self.agent is not None:
            if (
                pygame.sprite.spritecollide(self.agent, self.moving_shark, False, pygame.sprite.collide_mask)
                or pygame.sprite.spritecollide(self.shark, self.moving_ai, False, pygame.sprite.collide_mask)
            ):
                self.shark.rect.x = randint(1000, 1400)  # Move the shark to a new position
                self.two_players = False

        if self.shark.rect.x <= -150:
            self.shark.rect.x = randint(1000, 1400)  # Move the shark to a new position

        if self.player.rect.colliderect(self.bomb):
            if self.two_players == False:
                print("FIM DE JOGO!")
                return 0, self.score, self.hi_score

        
        if (pygame.sprite.spritecollide(self.player, self.moving_shark, False, pygame.sprite.collide_mask)):
            if self.two_players == False:
                print("FIM DE JOGO!")
                return 0, self.score, self.hi_score

        pygame.display.update()
        return 1, self.score,self.hi_score
        #return self.get_state(), self.calculate_reward(), self.is_game_over()


    def render_scores(self):


        placar = self.test_font.render("SCORE " + str(int(self.score)), False, self.ORANGE)
        placar_shadow = self.test_font.render("SCORE " + str(int(self.score)), False, self.BROWN)
        hi_placar = self.test_font.render("HI " + str(int(self.hi_score)), False, self.ORANGE)
        hi_placar_shadow = self.test_font.render("HI " + str(int(self.hi_score)), False, self.BROWN)
        self.screen.blit(hi_placar_shadow, (20, 24))
        self.screen.blit(hi_placar, (20, 20))

        self.screen.blit(placar_shadow, (hi_placar.get_rect().right +100, 24))
        self.screen.blit(placar, (hi_placar.get_rect().right +100, 20))
    
        #self.screen.blit(self.player.image, self.player.rect.topleft)

    ####################################
    #           METODOS DA IA          #
    ####################################

    def reset(self):
        #initialize game state
        self.score = 0
        self.scroll = 0
        self.background.draw_bg(self.scroll)
        self.background.draw_ground(self.scroll)
        self.render_scores

        if self.agent is not None:
            self.agent = AIPlayer(400,520,'sprites/ai_player', 0.05,0, state_size=4, action_size=2)
            self.moving_ai = pygame.sprite.Group()
            self.moving_ai.add(self.agent)
        
        self.moving_wave = pygame.sprite.Group()
        self.wave = Sprites(-9, 320, 'sprites/WAVE', 0.05, 0)
        self.moving_wave.add(self.wave)

        #Grupo de sprites da moeda
        self.moving_coin = pygame.sprite.Group()
        self.coin = Sprites(randint(600, 1000), 500, 'sprites/GoldCoinSprite', 0.15, 5)
        self.moving_coin.add(self.coin)

        #Grupo de sprites do tubarao
        self.moving_shark = pygame.sprite.Group()
        self.shark = Sprites(1400, 430, 'sprites/shark', 0.15, 10)
        self.moving_shark.add(self.shark)

    
    def calc_reward(self):
        reward = 0.0
        
        
        #if self.agent.rect[0] - self.shark.rect[0] < -290 and self.agent.is_jumping == False:
            #    print('recompensando por nao pular longe')
        #    reward = 0.2
        
        if self.agent.rect.colliderect(self.shark) == False:
            print('recompensando por nao colidir')
            reward = 1.0

        if self.agent.rect.colliderect(self.shark):
            print('punindo por colidir')
            reward = -1.0


        if self.agent.rect.left > self.shark.rect.right:
            print('Acertou o pulo')
            reward = 1.0


        return reward


    def is_game_over(self):
        if self.agent.rect.colliderect(self.shark):
            self.score = 0
            return True
        else:   
            return False



    def train(self, num_episodes):
        lst = len(os.listdir('runs/'))
        writer = SummaryWriter(f"runs/ml-model-test-{lst}")
        for episode in range(num_episodes):
            self.reset()
            done = False
            state = self.get_state()
            print(f'Game number {episode}/{num_episodes}')
            count = 0
            total_reward = 0

            while not done:
                count += 1

                action = self.agent.select_action(state)
                self.step(action)
                reward = self.calc_reward()
                next_state = self.get_state()

                total_reward += reward
                #print('Distance between objects:', self.agent.rect[0] - self.shark.rect[0])

                done = self.is_game_over()
                if done:
                    total_reward = 0
                    if self.score > self.hi_score:
                        self.hi_score = self.score
                    writer.add_text(f'Score Episode - {episode}', str(self.score))


                loss = self.agent.learn(state, action, reward, next_state, done)
                
                if loss != None:
                    writer.add_scalar("Loss/Train per episodes", loss, episode)
                state = next_state

        writer.add_text('HI_SCORE', str(self.hi_score))

        if not os.path.exists(f'runs/ml-model-test-{lst}/'):
            os.mkdir(f'runs/ml-model-test-{lst}/')
        torch.save({
            'model_state_dict': self.agent.q_network.state_dict(),
            'optimizer_state_dict': self.agent.optimizer.state_dict(),
        }, f'runs/ml-model-test-{lst}/model.pt')


if __name__ == "__main__":
    pygame.init()
    game = Game(0,0)

    #n = int(input('numero de partidas: '))
    while True:
        game.step()
    #game.run()
