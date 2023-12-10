import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.optimizers import Adam
from tf_agents.agents.dqn import dqn_agent
from Entities import TOTAL_INPUTS
from tf_agents.networks import sequential
import os


class HeroAgent:
    def __init__(self, tf_env):
        self._tf_env = tf_env
        self._build_agent()

    def _build_agent(self):
        q_net = sequential.Sequential([
            keras.layers.InputLayer(input_shape=(TOTAL_INPUTS,)),
            keras.layers.Dense(100, activation='relu'),
            keras.layers.Dense(4, activation=None),
        ])

        optimizer = Adam(learning_rate=1e-3)

        self.agent = dqn_agent.DqnAgent(
            self._tf_env.time_step_spec(),
            self._tf_env.action_spec(),
            q_network=q_net,
            optimizer=optimizer,
        )
        self.agent.initialize()
    
    def save_policy(self, model_path):
        os.makedirs(model_path, exist_ok=True)
        saved_model_path = os.path.join(model_path, 'saved_model')
        tf.saved_model.save(obj=self.agent.policy, export_dir=saved_model_path)
        
    def get_agent(self):
        return self.agent