'''
    credits for initial code and commenting to Sentdex
    originally developed as a solution for the CartPole enviorment provided by the gym libarry developed by Open AI using TFlearn
    https://pythonprogramming.net/openai-cartpole-neural-network-example-machine-learning-tutorial/
'''

import gym
import random
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter

import blackJack

LR = 1e-3

#enviorment requiers reset() step(action) render()
#enviorment also requires an action_space and observation_space

env = blackJack.Game()
#env = gym.make("CartPole-v0")

env.reset()
goal_steps = 500
score_requirement = 50
initial_games = 10000

if __name__ == '__main__':
    if False:
#    def some_random_games_first():
        # Each of these is its own game.
        for episode in range(5):
            env.reset()
            # this is each frame, up to 200...but we wont make it that far.
            for t in range(200):
                # This will display the environment
                # Only display if you really want to see it.
                # Takes much longer to display it.
                env.render()

                # This will just create a sample action in any environment.
                # In this environment, the action can be 0 or 1, which is left or right
                action = env.action_space.sample()

                # this executes the environment with an action,
                # and returns the observation of the environment,
                # the reward, if the env is over, and other info.
                observation, reward, done, info = env.step(action)
                if done:
                    break


#def initial_population():
    # [OBS, MOVES]
    training_data = []
    # all scores:
    scores = []
    # just the scores that met our threshold:
    accepted_scores = []
    # iterate through however many games we want:
    for _ in range(initial_games):
        score = 0
        # moves specifically from this environment:
        game_memory = []
        # previous observation that we saw
        prev_observation = []
        # for each frame in 200
        for _ in range(goal_steps):
            # choose random action (0 or 1)
            action = action = env.action_space.sample()
            # do it!
            observation, reward, done, info = env.step(action)

            # notice that the observation is returned FROM the action
            # so we'll store the previous observation here, pairing
            # the prev observation to the action we'll take.
            if len(prev_observation) > 0:
                game_memory.append([prev_observation, action])
            prev_observation = observation
            score += reward
            if done: break

        # IF our score is higher than our threshold, we'd like to save
        # every move we made
        # NOTE the reinforcement methodology here.
        # all we're doing is reinforcing the score, we're not trying
        # to influence the machine in any way as to HOW that score is
        # reached.
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                # convert to one-hot (this is the output layer for our neural network)
                if data[1] == 1:
                    output = [0, 1]
                elif data[1] == 0:
                    output = [1, 0]

                # saving our training data
                training_data.append([data[0], output])

        # reset env to play again
        env.reset()
        # save overall scores
        scores.append(score)

    # just in case you wanted to reference later
    training_data_save = np.array(training_data)
    np.save('saved.npy', training_data_save)

    # some stats here, to further illustrate the neural network magic!
    print('Average accepted score:', mean(accepted_scores)) #errors if accepted_scores is 0, implying that training failed
    print('Median score for accepted scores:', median(accepted_scores))
    print(Counter(accepted_scores))

#    return training_data
 #   training_data = initial_population()

#def train_model(training_data, model=False):
    model=False
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]), 1)
    y = [i[1] for i in training_data]

    if not model:
    #def neural_network_model(input_size):
        input_size = len(X[0])
        network = input_data(shape=[None, input_size, 1], name='input')

        network = fully_connected(network, 128, activation='relu')
        network = dropout(network, 0.8)

        network = fully_connected(network, 256, activation='relu')
        network = dropout(network, 0.8)

        network = fully_connected(network, 512, activation='relu')
        network = dropout(network, 0.8)

        network = fully_connected(network, 256, activation='relu')
        network = dropout(network, 0.8)

        network = fully_connected(network, 128, activation='relu')
        network = dropout(network, 0.8)

        network = fully_connected(network, 2, activation='softmax')
        network = regression(network, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy',
                             name='targets')
        model = tflearn.DNN(network, tensorboard_dir='log')

#        return model
#        model = neural_network_model(input_size=len(X[0]))

    model.fit({'input': X}, {'targets': y}, n_epoch=5, snapshot_step=500, show_metric=True, run_id='openai_learning')
#    return model
#    model = train_model(training_data)

    scores = []
    choices = []
    for each_game in range(10):
        score = 0
        game_memory = []
        prev_obs = []
        env.reset()
#        for _ in range(goal_steps):
        while True:
            env.render()

            if len(prev_obs) == 0:
                action = random.randrange(0, 2)
            else:
                action = np.argmax(model.predict(prev_obs.reshape(-1, len(prev_obs), 1))[0])

            choices.append(action)

            new_observation, reward, done, info = env.step(action)
            prev_obs = new_observation
            game_memory.append([new_observation, action])
            score += reward
            if done: break

        scores.append(score)

    print('Average Score:', sum(scores) / len(scores))
    print('choice 1:{}  choice 0:{}'.format(choices.count(1) / len(choices), choices.count(0) / len(choices)))
    print(score_requirement)