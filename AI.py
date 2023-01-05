import tensorflow as tf
import numpy as np
from tensorflow import keras
from keras.optimizers import Adam

    
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
