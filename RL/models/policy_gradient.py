# This code was generated by Microsoft CoPilot

import gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class PolicyNetwork(nn.Module):
    def __init__(self, n_inputs, n_actions):
        super(PolicyNetwork, self).__init__()
        self.fc = nn.Linear(n_inputs, n_actions)

    def forward(self, x):
        x = self.fc(x)
        return torch.softmax(x, dim=-1)


def select_action(policy, state):
    state = torch.from_numpy(state).float().unsqueeze(0)
    probs = policy(state)
    action = torch.multinomial(probs, 1).item()
    return action


def compute_returns(rewards, gamma=0.99):
    R = 0
    returns = []
    for r in reversed(rewards):
        R = r + gamma * R
        returns.insert(0, R)
    return returns


def train(policy, optimizer, env, episodes=1000):
    for episode in range(episodes):
        state = env.reset()
        rewards = []
        log_probs = []
        done = False

        while not done:
            action = select_action(policy, state)
            state, reward, done, _ = env.step(action)
            rewards.append(reward)
            log_prob = torch.log(policy(torch.from_numpy(state).float().unsqueeze(0))[0, action])
            log_probs.append(log_prob)

        returns = compute_returns(rewards)
        policy_loss = []
        for log_prob, R in zip(log_probs, returns):
            policy_loss.append(-log_prob * R)
        policy_loss = torch.cat(policy_loss).sum()

        optimizer.zero_grad()
        policy_loss.backward()
        optimizer.step()

        if episode % 50 == 0:
            print('Episode {}\tTotal reward: {:.2f}'.format(episode, np.sum(rewards)))


env_name = 'CartPole-v1'
env = gym.make(env_name)
n_inputs = env.observation_space.shape[0]
n_actions = env.action_space.n
policy = PolicyNetwork(n_inputs, n_actions)
optimizer = optim.Adam(policy.parameters(), lr=1e-2)
train(policy, optimizer, env)
