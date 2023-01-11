import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.optimizers import Adam
import reverb

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import py_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.policies import py_tf_eager_policy
from tf_agents.policies import random_tf_policy
from tf_agents.trajectories import trajectory
from tf_agents.specs import tensor_spec
from tf_agents.utils import common

from tf_agents.networks import sequential
from tf_agents.replay_buffers import reverb_replay_buffer
from tf_agents.replay_buffers import reverb_utils
    
def HeroDqn(learningRate,nActions,inputs, neuronsOne, neuronsTwo):
    inputLayer = keras.layers.Dense(inputs, input_shape=(8,))
    layerOne = keras.layers.Dense(neuronsOne, activation = 'relu')
    layerTwo = keras.layers.Dense(neuronsTwo, activation = 'relu')
    outputLayer = keras.layers.Dense(nActions, activation = None)
    model = keras.Sequential([inputLayer,layerOne,layerTwo,outputLayer])
    
    model.compile(optimizer = Adam(learning_rate=learningRate), loss = 'mean_squared_error')
    
    return model
# heroModel = HeroDqn(0.001,4,8,16,16)
# heroModel.predict([3,4,1,6,7,9,0,3])
# print(heroModel.summary())
