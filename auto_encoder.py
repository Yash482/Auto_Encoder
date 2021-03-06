import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

#get dataset
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', validation_size=0)

#plot 1 to check
img = mnist.train.images[2]
plt.imshow(img.reshape((28, 28)), cmap='Greys_r')

#building the requirements

#size of hidden layer(encoded layer)
encoding_dim = 32

img_size = mnist.train.images.shape[1]

#set input and target and both will be same
inputs_ = tf.placeholder(tf.float32, (None, img_size), name = 'inputs')
targets_ = tf.placeholder(tf.float32, (None, img_size), name = 'targets')

#encoded layer
encoded = tf.layers.dense(inputs_, encoding_dim, activation = tf.nn.relu)

#output layer logits
logits = tf.layers.dense(encoded, img_size, activation = None)

#sigmoid output form
decoded = tf.nn.sigmoid(logits, name = 'output')

#generate loss
loss = tf.nn.sigmoid_cross_entropy_with_logits(labels = targets_, logits = logits)
cost = tf.reduce_mean(loss)

#build optimizer
opt = tf.train.AdamOptimizer(0.001).minimize(cost)

#All requirements are done

#training-----------------

#create session
sess = tf.Session()

epochs = 20
batch_size = 200

sess.run(tf.global_variables_initializer())

for e in range(epochs):
    for i in range(mnist.train.num_examples // batch_size):
        batch = mnist.train.next_batch(batch_size)
        feed = {inputs_ : batch[0], targets_ : batch[0]}
        batch_cost, _ = sess.run([cost, opt], feed_dict = feed)
        
        print("Epoch : {}/{}...".format(e+1, epochs), "Training loss : {:4f}".format(batch_cost))


#visvualize results
fig, axes = plt.subplots(nrows=2, ncols=10, sharex=True, sharey=True, figsize=(20,4))
in_imgs = mnist.test.images[:10]
reconstructed, compressed = sess.run([decoded, encoded], feed_dict={inputs_: in_imgs})

for images, row in zip([in_imgs, reconstructed], axes):
    for img, ax in zip(images, row):
        ax.imshow(img.reshape((28, 28)), cmap='Greys_r')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)


fig.tight_layout(pad=0.1)