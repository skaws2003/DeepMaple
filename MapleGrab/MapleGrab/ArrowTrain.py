import tensorflow as tf
import numpy as np
import ArrowNet
import ArrowClassifier
import matplotlib.pyplot as plt
import random
import cv2
import glob

# Hyperparameters
learning_rate = 0.01
train_batch_size = 16
val_batch_size = 50
training_epoches = 500
saving_epoches = 10
ARROW_PATH = ArrowClassifier.ARROW_PATH
directions = ['left','right','up','down']
types = ['full','empty']

addrs = glob.glob(ARROW_PATH+"*.bmp")
random.shuffle(addrs)
labels = []
images = []
for addr in addrs:
    images.append(cv2.imread(addr))
    if 'left' in addr:
        if 'full' in addr:
            labels.append([1,0,0,0,0,0,0,0])
        elif 'empty' in addr:
            labels.append([0,1,0,0,0,0,0,0])
    if 'right' in addr:
        if 'full' in addr:
            labels.append([0,0,1,0,0,0,0,0])
        elif 'empty' in addr:
            labels.append([0,0,0,1,0,0,0,0])
    if 'up' in addr:
        if 'full' in addr:
            labels.append([0,0,0,0,1,0,0,0])
        elif 'empty' in addr:
            labels.append([0,0,0,0,0,1,0,0])
    if 'down' in addr:
        if 'full' in addr:
            labels.append([0,0,0,0,0,0,1,0])
        elif 'empty' in addr:
            labels.append([0,0,0,0,0,0,0,1])

for i in range(len(images)):
    images[i] = cv2.cvtColor(images[i], cv2.COLOR_BGR2HSV)

train_images = images[:int(0.6*len(images))]
train_labels = labels[:int(0.6*len(labels))]
val_images = images[int(0.6*len(images)):int(0.8*len(images))]
val_labels = labels[int(0.6*len(labels)):int(0.8*len(labels))]
test_images = images[int(0.8*len(images)):]
test_labels = labels[int(0.8*len(labels)):]

for _ in range(10):
    h,s,v = cv2.split(images[random.randint(0,len(images)-1)])
    #cv2.imshow('test',h)
    #cv2.waitKey(-1)
    #cv2.imshow('test',s)
    #cv2.waitKey(-1)
    cv2.imshow('test',v)
    cv2.waitKey(-1)

exit(0)
# Load Model
print("Initializing network...")
sess = tf.Session()
model = ArrowNet.ArrowCNN("ArrowNet")
sess.run(tf.global_variables_initializer())
try:
    model.restore(sess)
    print("Initializing done. Starting from epoch %d"%model.train_step)
except:
    print("Initializing failed. Starting from epoch 0")
    sess.run(tf.global_variables_initializer())


# Train!
print("Now start training...")
cost_log = []
accuracy_log = []
while model.train_step < training_epoches:
    # Training phase
    train_images_batch = []
    train_labels_batch = []
    for _ in range(train_batch_size):
        i = random.randint(0,len(train_images)-1)
        train_images_batch.append(train_images[i])
        train_labels_batch.append(train_labels[i])
    train_images_batch = np.stack(train_images_batch)
    train_labels_batch = np.stack(train_labels_batch)
    cost_log.append(model.train(sess=sess, x_data=train_images_batch, y_data=train_labels_batch))

    # Validation phase
    val_images_batch = []
    val_labels_batch = []
    for _ in range(val_batch_size):
        i = random.randint(0,len(val_images)-1)
        val_images_batch.append(val_images[i])
        val_labels_batch.append(val_labels[i])
    val_images_batch = np.stack(val_images_batch)
    val_labels_batch = np.stack(val_labels_batch)
    accuracy_log.append(model.get_accuracy(sess,val_images_batch,val_labels_batch))

    # Saving phase
    if (model.train_step%saving_epoches) == 0:
        model.save(sess)
        print("Saved training progress. %d/%d"%(model.train_step,training_epoches))

# Show Results
print(np.mean(accuracy_log))
plt.figure()
plt.plot(accuracy_log)
plt.show()