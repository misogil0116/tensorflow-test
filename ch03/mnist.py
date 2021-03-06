from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

# mnistデータを呼び出す
mnist = input_data.read_data_sets("../ch02/data/", one_hot=True)

# 入力データを定義する
x = tf.placeholder(tf.float32, [None, 784])
# 入力画像をログに出力する
img = tf.reshape(x, [-1, 28, 28, 1])
tf.summary.image("input_data", img, 10)

# 入力層 => 中間層
with tf.name_scope("hidden"):
  w_1 = tf.Variable(tf.truncated_normal([784, 64], stddev=0.1), name='w1')
  b_1 = tf.Variable(tf.zeros([64]), name='b1')
  h_1 = tf.nn.relu(tf.matmul(x, w_1) + b_1)

  # 中間層の重みの分布
  tf.summary.histogram("w_1", w_1)

# 中間層 => 出力層
with tf.name_scope("output"):
  w_2 = tf.Variable(tf.truncated_normal([64, 10], stddev=0.1), name='w2')
  b_2 = tf.Variable(tf.zeros([10]), name='b2')
  out = tf.nn.softmax(tf.matmul(h_1, w_2) + b_2)

y = tf.placeholder(tf.float32, [None, 10])
# 誤差関数
with tf.name_scope("loss"):
  loss = tf.reduce_mean(tf.square(y - out))

  # scalar => ログ取得
  tf.summary.scalar("loss", loss)

# 訓練
with tf.name_scope("train"):
  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss)

# 評価
with tf.name_scope("accuracy"):
  correct = tf.equal(tf.argmax(out, 1), tf.argmax(y, 1))
  accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

  # scalar => ログ取得
  tf.summary.scalar("accuracy", accuracy)

# 初期化
init = tf.global_variables_initializer()
summary_op = tf.summary.merge_all()

with tf.Session() as sess:
  summary_writer = tf.summary.FileWriter("logs", sess.graph)
  sess.run(init)

  # テストデータをロードする
  test_images = mnist.test.images
  test_labels = mnist.test.labels

  for i in range(1000):
    step = i + 1
    train_images, train_labels = mnist.train.next_batch(50)
    sess.run(train_step, feed_dict={x:train_images, y:train_labels})

    if i % 10 == 0:
      summary_str = sess.run(summary_op, feed_dict={x:test_images, y:test_labels})
      summary_writer.add_summary(summary_str, step)