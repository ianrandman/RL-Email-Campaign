import gym
import random


class EmailEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False):
        self.action_space = gym.spaces.Tuple((
            gym.spaces.Discrete(2),  # greeting
            gym.spaces.Discrete(2))  # salutation
        )

        self.observation_space = gym.spaces.Discrete(2)  # TODO demographic, etc?
        self.verbose = verbose
        self.human_feedback = 0
        self.state = 0  # TODO meaningless

    def step(self, action):
        if self.verbose:
            print('step')

        response_reward = random.choice([0, 1])  # whether there was a response TODO make not random
        reward = response_reward + self.human_feedback  # TODO wait for feedback

        done = False
        info = dict()

        return self.state, reward, done, info

    def reset(self):
        if self.verbose:
            print('reset')
        self.state = 0
        return self.state

    def render(self, mode='human'):
        if self.verbose:
            print('render')
        # TODO print email

    def close(self):
        if self.verbose:
            print('close')