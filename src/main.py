from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3 import A2C
from envs.email_env import EmailEnv

# multiprocess environment
n_cpu = 4

env = EmailEnv()
model = A2C("MlpPolicy", env, verbose=1)


def main():
    model.learn(total_timesteps=60)
    actions = list()

    obs = env.reset()
    for _ in range(100):
        action, _states = model.predict(obs)
        actions.append(action)
        obs, rewards, done, info = env.step(action)
        env.render()

    print(sum(actions))


if __name__ == '__main__':
    main()
