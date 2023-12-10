import tensorflow as tf
from tensorflow import keras
from keras.optimizers import Adam
from tf_agents.agents.dqn import dqn_agent
from tf_agents.networks import q_network,sequential
import os

class HeroAgent:
    def __init__(self, tf_env):
        self._tf_env = tf_env
        self._build_agent()

    def _build_agent(self):
        q_net = q_network.QNetwork(
            self._tf_env.observation_spec(),
            self._tf_env.action_spec(),
            fc_layer_params=(100,),
        )

        optimizer = Adam(learning_rate=1e-4)

        self.agent = dqn_agent.DqnAgent(
            self._tf_env.time_step_spec(),
            self._tf_env.action_spec(),
            q_network=q_net,
            optimizer=optimizer,
            td_errors_loss_fn=keras.losses.Huber(),
            train_step_counter=tf.Variable(0),
        )
        self.agent.initialize()
    
    def save_policy(self, model_path):
        os.makedirs(model_path, exist_ok=True)
        saved_model_path = os.path.join(model_path, 'saved_model')
        tf.saved_model.save(obj=self.agent.policy, export_dir=saved_model_path)
        
    def get_agent(self):
        return self.agent