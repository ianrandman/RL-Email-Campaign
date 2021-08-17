from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3 import A2C

from envs.email_env import EmailEnv

from backend import web
import threading


env = EmailEnv(verbose=False)
model = A2C("MlpPolicy", env, verbose=0)


def main():

    # start up the flask backend api
    app = web.get_webapp(env)
    threading.Thread(target=app.run, args=['0.0.0.0', 5000]).start()

    model.learn(total_timesteps=200)
    rewards = list()

    obs = env.reset()
    for _ in range(100):
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        rewards.append(reward)
        env.render()

    print(sum(rewards))


if __name__ == '__main__':
    main()
