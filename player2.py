import pygame
from random import randint
import torch
import torch.nn as nn
from game import Game  # Importe sua classe Game personalizada
import torch.optim as optim
from collections import deque


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.01





# Define a simple Q-network
class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)

    def forward(self, state):
        x = torch.relu(self.fc1(torch.tensor(state)))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class RLAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01):
        self.n_games = 0
        #randomness
        self.epsilon = epsilon
        #discount rate
        self.gamma = 0

        self.memory = deque(maxlen=MAX_MEMORY)
        self.state_size = state_size
        self.action_size = action_size
        self.q_network = QNetwork(state_size, action_size)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon


    def select_action(self, state):
        if torch.rand(1).item() < self.epsilon:
            return randint(0, self.action_size - 1)  # Explore
        else:
            with torch.no_grad():
                q_values = self.q_network(state)
                return q_values.argmax().item()  # Exploit

    def learn(self, state, action, reward, next_state, done):
        print(f'dimensoes do tensor: {state.size()}')

        q_values = self.q_network(state)

        next_q_values = self.q_network(next_state)
        max_next_q_value = next_q_values.max().unsqueeze(0)
        target_q_value = torch.tensor(reward) + self.gamma * max_next_q_value * torch.tensor(1)
        
        print(f'variavel q value: {q_values} \n variavel action: {torch.tensor([action])}\n variavel target value: {target_q_value}')
        loss = nn.MSELoss()(q_values[action], target_q_value)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay

def main():
    # Initialize your game class
    game = Game(use_ai=True)   # Instancie sua classe Game personalizada
    state_size = 4   # Obtenha o tamanho do estado do jogo
    action_size = 2  # Obtenha o tamanho do espaço de ação

    agent = RLAgent(state_size, action_size)

    for episode in range(10):  # Número de episódios
        state = torch.Tensor(game.reset())  # Reinicie o jogo e obtenha o estado inicial

        for time_step in range(10):  # Número máximo de etapas de tempo por episódio
            #old state
            state_old = game.get_state()

            #get move
            action = agent.select_action(state_old)

            #perfomm move and get new state
            next_state, reward, done = game.step(action=1)
            next_state = torch.Tensor(next_state)

            #train short
            agent.learn(state, action, reward, next_state, done)
            state = next_state

            if done:
                break

if __name__ == "__main__":
    main()
