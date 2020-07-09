import gym 
import numpy as np
from gym import wrappers

env = gym.make('CartPole-v0')

bestLenght = 0
episode_lenght = []

for i in range(100):
    new_weights =  np.random.uniform(-1.0, 1.0, 4)
    length = []
    for j in range(100):
        observation = env.reset()
        done = False
        cnt = 0
        while not done:
            cnt += 1 
            action = 1 if np.dot(observation, new_weights)>0 else 0 

            observation, reward, done , _ = env.step(action)

            if done:
                break
        length.append(cnt)
    average_length = float(sum(length)/len(length))

    if average_length > bestLenght:
        bestLenght = average_length
        best_weight = new_weights
    episode_lenght.append(average_length)
    if i % 10 == 0:
        print('best length is', bestLenght)
done = False
cnt = 0 
env = wrappers.Monitor(env, 'MovieFiles2', force=True)
observation = env.reset()

while not done:
            cnt += 1 
            action = 1 if np.dot(observation, new_weights)>0 else 0 

            observation, reward, done , _ = env.step(action)

            if done:
                break
print('game finished:', cnt, 'moves')

