import gym


class EmailEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False):
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Discrete(2)
        self.verbose = verbose

    def step(self, action):
        if self.verbose:
            print('step')

        state = 1

        if action == 1:
            reward = 1
        else:
            reward = -1

        done = False
        info = dict()

        return state, reward, done, info

    def reset(self):
        if self.verbose:
            print('reset')
        return 0

    def render(self, mode='human'):
        if self.verbose:
            print('render')

    def close(self):
        if self.verbose:
            print('close')