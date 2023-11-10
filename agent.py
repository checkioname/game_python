import pygame
from random import randint
from sprites import Sprites
import torch
import torch.nn as nn
from collections import deque
from torch.optim import Adam
from random import randint, sample

MAX_MEMORY = 10000

class AIPlayer(Sprites):

    def __init__(self, pos_x, pos_y, player_path, current_sprite, run_speed, state_size, action_size, epsilon_decay=0.5, min_epsilon=0.01, gamma=0.99,replay_buffer_size=20000):
        super().__init__(pos_x, pos_y, player_path, current_sprite, run_speed)
        self.is_jumping = False
        self.jump_vel = 8.5
        self.jump_sprites = []
        self.jump_sprites.append(pygame.image.load('sprites/ai_player/jump/image_8.png'))
        self.jump_sprites.append(pygame.image.load('sprites/ai_player/jump/image_9.png'))
        
        #####################
        # Parâmetros da IA #
        ###################

        self.q_network = QNetwork(state_size, action_size)
        self.target_q_network = QNetwork(state_size, action_size)
        self.target_q_network.load_state_dict(self.q_network.state_dict())
        self.optimizer = Adam(self.q_network.parameters(), lr=0.001)
        self.epsilon = 1.0
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.gamma = gamma
        self.replay_buffer_size = replay_buffer_size
        self.replay_buffer = deque(maxlen=self.replay_buffer_size)
        self.batch_size = 64  # You can adjust this according to your needs
        self.global_step = 0
        self.target_update_freq = 100  # Update target network every 100 steps

        #load train weights
        #checkpoint = torch.load('runs/ml-model-test-117/model.pt')
        #self.q_network.load_state_dict(checkpoint['model_state_dict'])
        #self.target_q_network.load_state_dict(checkpoint['model_state_dict'])



    def jump(self):
        if self.is_jumping:
            self.image = self.jump_sprites[0]
            self.rect.y -= self.jump_vel * 2.5
            self.jump_vel -= 0.40

        if self.jump_vel <= 0:
            self.image = self.jump_sprites[1]

        if self.jump_vel < -8.5:
            self.rect.y = 500
            self.is_jumping = False
            self.jump_vel = 8.5


        


    def make_decision(self):
        if self.rect.y < 400: 
            return 1  # Pular
        else:
            return 0  # Não fazer nada

    
    def select_action(self, state):
        state_tensor = torch.tensor(state, dtype=torch.float)
        if torch.rand(1).item() < self.epsilon:
            return randint(0, 1)  # Explore
        else:
            with torch.no_grad():
                action = self.q_network(state_tensor)
                print("Q-values:", action)  # Add this line for debugging
                return action.argmax().item()  # Exploit



    #funcao de treino antiga sem 

    #def learn(self, state, action, reward, next_state, done):
    #        state_tensor = torch.tensor(state, dtype=torch.float)
    #        next_state_tensor = torch.tensor(next_state, dtype=torch.float)
#
    #        q_values = self.q_network(state_tensor)
    #        next_q_values = self.q_network(next_state_tensor)
    #        max_next_q_value = next_q_values.max().unsqueeze(0)
#
    #        target_q_value = torch.tensor(reward, dtype=torch.float) + self.gamma * max_next_q_value
#
    #        loss = nn.MSELoss()(q_values[action], target_q_value)
#
    #        self.optimizer.zero_grad()
    #        loss.backward()
    #        self.optimizer.step()
    #        #print(f'Loss {loss.item():.4f}')
    #        if self.epsilon > self.min_epsilon:
    #            self.epsilon *= self.epsilon_decay
#
    #        return loss

    def learn(self, state, action, reward, next_state, done):
        # Store experience in replay buffer
        self.replay_buffer.append((state, action, reward, next_state, done))

        # Sample a batch from the replay buffer
        if len(self.replay_buffer) >= self.batch_size:
            batch = sample(self.replay_buffer, self.batch_size)
            states, actions, rewards, next_states, dones = zip(*batch)

            # Convert to tensors
            state_tensor = torch.tensor(states, dtype=torch.float)
            next_state_tensor = torch.tensor(next_states, dtype=torch.float)

            # Compute Q-values for current and next states
            q_values = self.q_network(state_tensor)
            next_q_values = self.q_network(next_state_tensor)
            max_next_q_value = next_q_values.max(dim=1, keepdim=True)[0]

            # Compute target Q-value using the Bellman equation
            targets = torch.tensor(rewards, dtype=torch.float).view(-1, 1) + \
                      self.gamma * max_next_q_value * (1 - torch.tensor(dones, dtype=torch.float).view(-1, 1))

            # Compute the loss
            loss = nn.MSELoss()(q_values.gather(1, torch.tensor(actions).view(-1, 1)), targets)
            #print('valor da loss function: ',loss.item())

            if loss is not None and not torch.isnan(loss).any():
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                # Update epsilon
                if self.epsilon > self.min_epsilon:
                    self.epsilon *= self.epsilon_decay

                print("Loss:", loss.item())
            else:
                print("Loss nula:", loss.item())


            return loss



class QNetwork(nn.Module):
    torch.manual_seed(42)
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 20)    
        self.fc2 = nn.Linear(20, 8)
        self.fc3 = nn.Linear(8, action_size)

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
