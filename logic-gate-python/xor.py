import tensorflow as tf
from tensorflow.python.framework.graph_util import convert_variables_to_constants


def main():
    input = [[0, 0], [0, 1], [1, 0], [1, 1]]
    labels = [[0], [1], [1], [0]]

    x = tf.placeholder(tf.float32, shape=[None, 2])
    y = tf.placeholder(tf.float32, shape=[None, 1])

    HIDDEN_NODES = 5

    w_hidden = tf.Variable(tf.random_uniform([2, HIDDEN_NODES], -0.1, 1.0), name='w_hidden')
    b_hidden = tf.Variable(tf.zeros([HIDDEN_NODES]), name='b_hidden')
    hidden = tf.nn.relu(tf.matmul(x, w_hidden) + b_hidden, name='hidden')

    w_output = tf.Variable(tf.random_uniform([HIDDEN_NODES, 1], -0.1, 1.0), name='w_output')
    b_output = tf.Variable(tf.zeros([1]), name='b_output')
    y_pred = tf.sigmoid(tf.matmul(hidden, w_output) + b_output, name='y_pred')

    loss = -tf.reduce_sum(y * tf.log(y_pred) + (1 - y) * tf.log(1 - y_pred), name='loss')
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1, name='optimizer')
    train_step = optimizer.minimize(loss, name='train_step')

    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        for epoch in range(1001):
            _, l = session.run(
                [train_step, loss],
                feed_dict={x: input, y: labels}
            )

            if epoch % 100 == 0:
                print("epoch: {}, loss: {}".format(epoch, l))

        for data in input:
            print("[TEST] input: {} | output: {}".format(data, session.run(y_pred, feed_dict={x: [data]})))

        graph_def = convert_variables_to_constants(session, session.graph_def, ['train_step'])
        tf.train.write_graph(graph_def, 'models', 'xor.pb', as_text=False)
        tf.train.write_graph(graph_def, 'models', 'xor.pb.txt', as_text=True)


if __name__ == '__main__':
    main()
