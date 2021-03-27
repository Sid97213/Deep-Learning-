# -*- coding: utf-8 -*-
"""LogisticReg_Scratch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZIHzCaYwRvVGvj8pdK7DYw_o00LPBiUm
"""

# https://builtin.com/data-science/guide-logistic-regression-tensorflow-20

import numpy as np
import tensorflow as tf
# from tensorflow import keras
from __future__ import absolute_import,division, print_function
# from keras.utils import to_categorical
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import mnist

(x_train, y_train),(x_test,y_test) = mnist.load_data()
# Convert to float32
x_train, x_test = np.array(x_train,np.float32),np.array(x_test, np.float32)

num_features= 784
# Flatten images to 1-D vector of 784
x_train, x_test = x_train.reshape([-1,num_features]), x_test.reshape([-1,num_features])

# Normalize images value from [0,255] to [0,1]
x_train, x_test = x_train/255., x_test/255.

num_classes = 10
num_features = 784
learning_rate = 0.01
training_steps = 1000
batch_size = 256
display_step = 50

# batch the data
train_data = tf.data.Dataset.from_tensor_slices((x_train,y_train))

train_data = train_data.repeat().batch(batch_size).prefetch(1)
# If shuffle required-
# train_data = train_data.repeat().shuffle(5000).batch(batch_size).prefetch(1)

# Intializing weights and biases
W = tf.Variable(tf.ones([num_features,num_classes]), name = "weight")

# Bias of shape [10], total number of classes
b = tf.Variable(tf.zeros([num_classes]),name = "bias")

# Defining LR and cost function
def logistic_regression(x):
  # Apply softmax to normalize the logits to a probability distribution
  return tf.nn.softmax(tf.matmul(x,W)+b)

def cross_entropy(y_pred,y_true):
  # Encode label to a one-hot vector
  y_true = tf.one_hot(y_true, depth=num_classes)
  # Clip prediction valeus to avoid log(0) error
  y_pred = tf.clip_by_value(y_pred,1e-9,1.)
  # Compute cross_entropy
  return tf.reduce_mean(-tf.reduce_sum(y_true*tf.math.log(y_pred)))

# defining optimizers and accuracy metrics
def accuracy(y_pred,y_true):
  correct_prediction = tf.equal(tf.argmax(y_pred,1), tf.cast(y_true,tf.int64))
  return tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

# Stochastic gradient descent optimizer
optimizer = tf.optimizers.SGD(learning_rate)

# Optimization process and updating weights and biases
def run_optimization(x,y):
  # wrap computation inside a GradientTape for automatic differentiation
  with tf.GradientTape() as g:
    pred = logistic_regression(x)
    loss = cross_entropy(pred,y)
  # Compute gradients
  gradients = g.gradient(loss,[W,b])

  # update W and b following gradients
  optimizer.apply_gradients(zip(gradients,[W,b]))

# Training loop
for step, (batch_x, batch_y) in enumerate(train_data.take(training_steps),1):
  # Run the optimization to update W and b values
  run_optimization(batch_x, batch_y)
  if step % display_step == 0:
    pred = logistic_regression(batch_x)
    loss = cross_entropy(pred,batch_y)
    acc = accuracy(pred, batch_y)
    print("step: {}, loss: {}, accuracy: {}".format(step, loss, acc))
    # unnecessary
    pred = logistic_regression(x_test)
    test_acc = accuracy(pred,y_test)
    print("Test Accuracy: {}".format(test_acc))
    if (test_acc > 0.92):
      break

# Testing model on validation set
pred = logistic_regression(x_test)
print("Test Accuracy: {}".format(accuracy(pred,y_test)))

# best test accuracy 0.9236000

