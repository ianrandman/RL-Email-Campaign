from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3 import A2C

from envs.email_env import EmailEnv

from backend import web
import threading


# initiate environment and RL agent
env = EmailEnv(verbose=False)
model = A2C("MlpPolicy", env, verbose=0)


def main():

    # start up the flask backend api
    app = web.get_webapp(env)
    threading.Thread(target=app.run, args=['0.0.0.0', 5000]).start()

    model.learn(total_timesteps=200)

    # evaluate for 100 emails and see total reward
    total_reward = 0
    obs = env.reset()
    for _ in range(100):
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        env.render()

    print(total_reward)


if __name__ == '__main__':
    main()
