#import the necessary libraries
import numpy as np
import random  #helps us to setup random values

#environment setup
road_length = 5 #number os steps to move (0-4) index
action = ['right', 'left'] #steps to move 

#Q-table intialisation
Q = np.zeros((road_length, len(action)))

#hyperparameter
episodes = 1000 #the bigger the nuber of episodes the higher the learning chances of the model
learning_rate = 0.8
gamma = 0.9  #it will have a higer reward
epislon = 0.3  #helps the agent to discover the new path

#training episodes
for episode in range(episodes):
    state = 0

    while state !=4:
        if random.uniform(0,1) < epislon:
            action = random.randint(0,1)
        else:
            action= np.argmax(Q[state])


