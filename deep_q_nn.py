# Deep Q Network for playing Shark Invaders

from __future__ import print_function

import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()

import cv2
import sys
import game
import random
import numpy as np
from collections import deque

GAME = "shark"
ACTIONS = 4
GAMMA = 0.99
OBSERVE = 100000.
EXPLORE = 2000000.
FINAL_EPS = 0.0001
INITIAL_EPS = 0.0001
REPLAY_MEMORY = 50000
BATCH = 32
FRAME_PER_ACTION = 1


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.01)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.01, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides=[1, stride, stride, 1], padding="SAME")


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")


def createNetwork():
    # network weights
    w_conv1 = weight_variable([8, 8, 4, 32])
    b_conv1 = bias_variable([32])

    w_conv2 = weight_variable([4, 4, 32, 64])
    b_conv2 = bias_variable([64])

    w_conv3 = weight_variable([3, 3, 64, 64])
    b_conv3 = bias_variable([64])

    w_fc1 = weight_variable([1600, 512])
    b_fc1 = bias_variable([512])

    w_fc2 = weight_variable([512, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # input layer
    s = tf.placeholder("float", [None, 80, 80, 4])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(s, w_conv1, 4) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2, 2) + b_conv2)
    # h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_conv2, w_conv3, 1) + b_conv3)
    # h_pool3 = max_pool_2x2(h_conv3)

    # h_pool3_flat = tf.reshape(h_pool3, [-1, 256])
    h_conv3_flat = tf.reshape(h_conv3, [-1, 1600])

    h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, w_fc1) + b_fc1)

    # readout layer
    readout = tf.matmul(h_fc1, w_fc2) + b_fc2

    return s, readout, h_fc1
