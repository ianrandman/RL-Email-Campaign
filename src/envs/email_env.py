import json

import gym
import random
from time import sleep


greetings = {
    0: 'Hello Customer,\n\n',
    1: "sup\n\n"
}

salutations = {
    0: 'Respectfully,\nCustomer Support',
    1: 'see ya later alligator'
}


class EmailEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False):
        self.action_space = gym.spaces.MultiDiscrete((
            2,  # greeting
            2)  # salutation
        )

        self.observation_space = gym.spaces.Discrete(1)  # TODO demographic, etc?
        self.verbose = verbose

        self.email = None
        self.human_feedback = None

    def step(self, action):
        if self.verbose:
            print('step')

        self.email = greetings[action[0]] + salutations[action[-1]]

        response_reward = random.choice([0, 1])  # whether there was a response TODO make not random

        while self.human_feedback is None:
            sleep(0.1)
        reward = response_reward + self.human_feedback  # TODO wait for feedback

        done = True
        info = dict()

        return 0, reward, done, info

    def reset(self):
        if self.verbose:
            print('reset')
        self.email = None
        self.human_feedback = None
        return 0

    def render(self, mode='human'):
        if self.verbose:
            print('render')
        print(self.email)

    def close(self):
        if self.verbose:
            print('close')

    # def clear_jsons(self):
    #     with open('data/email.json', 'w') as f:
    #         json.dump(dict(), f)
    #     with open('data/feedback.json', 'w') as f:
    #         json.dump(dict(), f)
