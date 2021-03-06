import tensorflow as tf
import tensorflow.contrib.layers as tfc_layers


class Regularizer(object):

    def __init__(self, config, is_training, dropout_keep,reuse):
        self.config = config
        self._is_training = is_training
        self.dropout_keep = dropout_keep
        self.reuse = reuse

    def apply(self, node, name):
        current_scope = tf.contrib.framework.get_name_scope()

        with tf.variable_scope(name):

            if any([node in current_scope for node in self.config['dropout_list']]):
                node = tf.nn.dropout(node, self.dropout_keep)

            elif any([node in current_scope for node in self.config['batchnorm_list']]):
                node = tfc_layers.batch_norm(node, is_training=self._is_training, reuse=self.reuse)

        return node

    def __call__(self, node, name):
        return self.apply(node, name)