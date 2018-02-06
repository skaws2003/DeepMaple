import tensorflow as tf
import numpy as np

class ArrowCNN:

    def __init__(self,name):
        self.name = name
        self.build_net()
        self.saver = tf.train.Saver()
        self.train_step = 0
        self.save_path = 'D:/tfrecords/'

    def build_net(self):
        with tf.variable_scope(self.name):
            # Variables
            drop_rate = 0.7
            learning_rate = 0.01
            
            # Placeholders
            self.X = tf.placeholder(tf.float32,[None,61,61,3])
            self.Y = tf.placeholder(tf.float32,[None,8])
            self.is_training = tf.placeholder(tf.bool)
            xavier_initializer = tf.contrib.layers.xavier_initializer()
            # Layers
            self.conv1 = tf.layers.conv2d(inputs=self.X, filters=16, kernel_size=[3,3], activation=tf.nn.relu, name="conv1", kernel_initializer=xavier_initializer)
            self.pool1 = tf.layers.max_pooling2d(inputs=self.conv1,pool_size=[2,2],strides=2)
            self.conv2 = tf.layers.conv2d(inputs=self.pool1, filters=32, kernel_size=[5,5], activation=tf.nn.relu, name="conv2", kernel_initializer=xavier_initializer)
            self.dropout1 = tf.layers.dropout(inputs=self.conv2,rate=drop_rate,training=self.is_training,name="dropout1")
            self.flat1 = tf.reshape(self.dropout1, [-1,25*25*32])
            self.dense1 = tf.layers.dense(inputs=self.flat1,units=512,activation=tf.nn.relu,name="dense1")
            self.dropout2 = tf.layers.dropout(inputs=self.dense1,rate=drop_rate,training=self.is_training,name="dropout2")
            self.logits = tf.layers.dense(inputs=self.dropout2, units=8, name="logits")
            self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.Y))
            self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)
            self.correct_prediction = tf.equal(tf.argmax(self.logits, 1), tf.argmax(self.Y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))
            
    def predict(self, sess, x_test, training=False):
        return sess.run(self.logits,feed_dict={self.X: x_test, self.is_training: training})

    def get_accuracy(self, sess, x_test, y_test, training=False):
        return sess.run(self.accuracy,feed_dict={self.X: x_test,self.Y: y_test, self.is_training: training})

    def train(self, sess, x_data, y_data, training=True):
        self.train_step += 1
        return sess.run([self.cost, self.optimizer], feed_dict={self.X: x_data, self.Y: y_data, self.is_training: training})

    def save(self, sess):
        self.saver.save(sess=sess, save_path=self.save_path+"ArrowNet", global_step=self.train_step)

    def restore(self,sess):
        self.saver.restore(sess,tf.train.latest_checkpoint('D:/tfrecords/'))

