# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import os.path
import time

import numpy as np
from six.moves import xrange
import tensorflow as tf

import CNN
import CNN_test
FLAGS = tf.app.flags.FLAGS

#tf.app.flags.DEFINE_string('train_dir', 'F:\\code\\cifar10_train',
#                           """Directory where to write event logs """
#                           """and checkpoint.""")
tf.app.flags.DEFINE_string('train_dir', '/home/tuxiang/桌面/code/cifar10_train',
                           """Directory where to write event logs """
                           """and checkpoint.""")
tf.app.flags.DEFINE_integer('max_steps', 100000,
                            """Number of batches to run.""")
tf.app.flags.DEFINE_boolean('log_device_placement', False,
                            """Whether to log device placement.""")

def train():
    with tf.Graph().as_default():
        global_step = tf.Variable(0,trainable=False)

        images,labels = CNN.distorted_inputs()
        logits = CNN.cnn_model(images)
        print(logits.get_shape())
        print(logits.get_shape())
        print(labels.get_shape())
        loss = CNN.loss(logits,labels)
        train_op = CNN.train(loss,global_step,True)

        train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)  # 添加

        saver = tf.train.Saver(tf.global_variables())
        summary_op = tf.summary.merge_all()
        init = tf.global_variables_initializer()

        sess = tf.Session(
            config=tf.ConfigProto(log_device_placement=FLAGS.log_device_placement)
        )
        sess.run(init)

        tf.train.start_queue_runners(sess=sess)

        summary_writer = tf.summary.FileWriter(FLAGS.train_dir,sess.graph)

        for step in range(FLAGS.max_steps):
            start_time = time.time()
            _,loss_value = sess.run([train_op,loss])
            duration = time.time() - start_time

            assert not np.isnan(loss_value),'Model diverged with loss = NaN'

            if step % 500 == 0:
                summary_str = sess.run(summary_op)
                summary_writer.add_summary(summary_str,step)
                num_examples_per_step = FLAGS.batch_size
                example_per_sec = num_examples_per_step / duration
                sec_per_batch = float(duration)
                format_str = ('%s;step %d,loss = %.2f (%.1f example/sec; %.3f sec/batch)')
                print(format_str %(datetime.now(),step,loss_value,example_per_sec,sec_per_batch))

                #添加

                summary_writer = tf.summary.FileWriter(FLAGS.train_dir, sess.graph)
                summary_writer.add_summary(sess.run(summary_op), step)
                sess.run(train_step)

                #添加画出精度曲线
                CNN_test.evaluate()

            if step % 5000 == 0 or (step + 1) == FLAGS.max_steps:  #1000改为了100
                checkpoint_path = os.path.join(FLAGS.train_dir,'model.ckpt')
                saver.save(sess,checkpoint_path,global_step=step)



def main(argv=None):
    #CNN.maybe_download_and_extract()
    #if tf.gfile.Exists(FLAGS.train_dir):
    #    tf.gfile.DeleteRecursively(FLAGS.train_dir)
    #tf.gfile.MakeDirs(FLAGS.train_dir)
    train()

if __name__ == '__main__':
    tf.app.run()
        
