import tensorflow as tf
import numpy as np

class ArrowNet:

    def __init__(self,sess,name):
        self.sess = sess
        self.name = name
        self.build_net()

    def build_net(self):
        with tf.variable_scope(self.name):
            # Variables
            drop_rate = 0.7
            

            # Placeholders
            self.X = tf.placeholder(tf.float32,[None,61,61,3])
            self.Y = tf.placeholder(tf.float32,[None,4])
            self.is_training = tf.placeholder(tf.bool)
            xavier_initializer = tf.contrib.layers.xavier_initializer()
            # Layers
            conv1 = tf.layers.conv2d(inputs=self.X, filters=16, kernel_size=[3,3], activation=tf.nn.relu, name="conv1", kernel_initializer=xavier_initializer)
            pool1 = tf.layers.max_pooling2d(inputs=conv1,pool_size=[2,2],strides=2)
            conv2 = tf.layers.conv2d(inputs=pool1, filters=32, kernel_size=[5,5], activation=tf.nn.relu, name="conv2", kernel_initializer=xavier_initializer)
            dropout1 = tf.layers.dropout(inputs=conv2,rate=drop_rate,training=self.is_training,name="dropout1")
            flat1 = tf.reshape(dropout1, [-1,25*25*32])
            dense1 = tf.layers.dense(inputs=flat1,units=512,activation=tf.nn.relu,name="dense1")
            dropout2 = tf.layers.dropout(inputs=dense1,rate=drop_rate,training=self.is_training,name="dropout2")
            self.logits = tf.layers.dense(inputs=dropout2, units=4, name="logits")
            self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.Y))
            self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)
            correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            
    def predict(self, x_test, training=False):
        return self.sess.run(self.logits,feed_dict={self.X: x_test, self.training: training})

    def get_accuracy(self, x_test, y_test, training=False):
        return self.sess.run(self.accuracy,feed_dict={self.X: x_test,self.Y: y_test, self.training: training})

    def train(self, x_data, y_data, training=True):
        return self.sess.run([self.cost, self.optimizer], feed_dict={self.X: x_data, self.Y: y_data, self.training: training})

