# -*- coding: utf-8 -*-
"""BasicNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y6vGxxbru0YgfH5FqBEKEdlo1-Axjzhf
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt

print("tensorflow version: ",tf.__version__)
tf.test.gpu_device_name()
# to test whether GPU is being used.

# tensorflow.keras has the mnist dataset already loaded and ready for use, we just import it.
# It is the same as downloading from the actual site.
digit_dataset = tf.keras.datasets.mnist
(train_images,train_labels), (test_images, test_labels) = digit_dataset.load_data()

# data is 60000 training images and labels, 10000 testing images and labels.
# single image is of 28-by-28 dimension, with each of those 784 values ranging from 0 to 255
# here we normalize the training and testing images data.
(train_images), (test_images) = train_images/255,test_images/255

# An example of training image
plt.imshow(train_images[989])

train_labels[989]

"""The following is the model of Neural Network with 1 hidden layer.
'[Sequential](https://keras.io/api/models/sequential/)' is just to denote a series of layers in a sequence.
The NN contains an input layer in the beginning, and an output layer in the end. The input layer is 'Flatten' because our input is in a grid of 28by28, so we flatten each input image out to single 784by1 vector and pass it in.
'[Dense](https://keras.io/api/layers/core_layers/dense/)' layers are the regular layers, providing straightforward application of the activation function on the (dot product x'.w  + bias). Number of units in that layer is the first argument, and the activation function is to be specified.
Output layer has activation 'softmax' because we are doing multiclass classification. This most probably wont change throughout all our NNs.
Adding more layers can be done by adding the code for each, separated by commas in the way it is done below.

"""

# keras.layers.Dense(num_of_units,activation='relu')
# keras.layers.LeakyReLU(alpha=0.3)
# keras.layers.PReLU(alpha_initializer='zeros')
model = keras.Sequential([
                          keras.layers.Flatten(input_shape=(28,28)),
                          keras.layers.Dense(10,activation='relu'),
                          keras.layers.Dense(10,activation='softmax')
])

# a summary of what our NN is doing in each layer. First layer flattens, second layer applies ReLU, last layer applies Softmax
model.summary()

# optimizer can be stochastic gradient descent ('sgd') or Adam (works better).
# loss function wont change because we are dealing with multiclass problem. crossentropy was discussed in class.
# metrics just informs the compiler what to display additionally while training
model.compile(optimizer='adam',loss = 'sparse_categorical_crossentropy',metrics = ['accuracy'])

# num_epochs is the number of epochs we want to train for.
num_epochs=10
# we fit (train) the model we made
fitting = model.fit(train_images,train_labels,epochs=num_epochs,verbose=1)

# model has been trained, some parameters have been learnt
# Now we evaluate the learned parameters on the 10000 unseen images
# eval = model.evaluate(test_images,test_labels)
eval[-1]

acc = fitting.history['accuracy']
loss = fitting.history['loss']

epochs = range(num_epochs)
plt.plot(epochs,acc,'b',label='Training Accuracy')
plt.plot(epochs,loss,'r',label='Training Loss')

plt.plot(epochs,loss,'r',label='Training Loss')

