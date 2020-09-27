import tensorflow as tf
import numpy as np
import cv2

def Compiler():
    mnist = tf.keras.datasets.mnist

    # loads in MNIST digit classification data and assigns variables
    (training_data, training_labels), (test_data, test_labels) = mnist.load_data()

    # converts pixels to float for better reconigtion
    training_data = training_data / 255

    # biulds neural network with input and essentially leading to probability of a the possible 10 digits to be output
    mod = tf.keras.Sequential([tf.keras.layers.Flatten(input_shape=(28, 28)), tf.keras.layers.Dense(128, activation=tf.nn.relu), tf.keras.layers.Dense(10, activation=tf.nn.softmax)])

    # setup for compilation of the model, sparse_categorical_crossentropy
    mod.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # training of data and labels using and epoch of 4 "4 loops essentially"
    mod.fit(training_data, training_labels, epochs=4)
    return mod

def imageGray(img):
    # reading image and converting to grayscale
    numimage = cv2.imread(img)
    grayscale = cv2.cvtColor(numimage, cv2.COLOR_BGR2GRAY)
    return grayscale


def readNums(g):
    # turns image into a binary image and find the curve "contour" that numbers are made with
    ret, th1 = cv2.threshold(g, 127, 255, cv2.THRESH_BINARY_INV)
    contours, h = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final = []
    for i in contours:
        # assigns bounding rectangle for each letter found
        x,y,w,h = cv2.boundingRect(i)

        # obtains top right and bottom left corner of the digit being analyzed
        corner_1 = (x,y)
        corner_2 = (x+w, y+h)

        # cuts digit from background
        digit = th1[corner_1[1]:corner_2[1], corner_1[0]:corner_2[0]]

        # resizes to more closely resemable test case digits
        resize_frame = cv2.resize(digit, (18,18))
        add_pad = np.pad(resize_frame, ((5,5),(5,5)), "constant", constant_values=0)
        final.append(add_pad)
    return final

