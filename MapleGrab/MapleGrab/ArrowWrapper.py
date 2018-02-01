import tensorflow as tf
import numpy as np
from random import shuffle
import glob
import cv2
import ArrowTagger

"""

This turns arrow images to .tfrecords
Not on develop now: there are very few data(~4000 pics) so there is less reason to speed up training
Might do it later.

"""


# Variables
train_filename = './tfrecords/minigame_arrows.tfrecords'
TAG_PATH = ArrowTagger.TAG_PATH

# Open arrow images and shuffle
addrs = glob.glob(TAG_PATH)
labels = [0 if 'left' in addr else 1 if 'right' in addr else 2 if 'up' in addr else 3 for addr in addrs]
c = list(zip(addrs,labels))
shuffle(c)
addrs,labels = zip(*c)

# Divide: 60% train 20% validation 20% test
train_addrs = addrs[0:int(0.6*len(addrs))]
train_labels = labels[0:int(0.6*len(labels))]
val_addrs = addrs[int(0.6*len(addrs)):int(0.8*len(addrs))]
val_labels = labels[int(0.6*len(addrs)):int(0.8*len(addrs))]
test_addrs = addrs[int(0.8*len(addrs)):]
test_labels = labels[int(0.8*len(labels)):]

writer = tf.python_io.TFRecordWriter(train_filename)