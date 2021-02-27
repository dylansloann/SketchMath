import tensorflow as tf
import numpy as np
import cv2

def Compiler():
    dataMNIST = tf.keras.datasets.mnist

    # loads in MNIST digit classification data and assigns variables for training and testing
    # will not be using testing data in this as do not need to evaluate
    (trainData, trainLabels), (testData, testLabels) = dataMNIST.load_data()

    # converts pixels that are on scale [0, 255] to float for better reconigtion
    trainData = trainData / 255

    # biulds neural network with input and essentially leading to probability of a the possible 10 digits to be output
    # with one hidden layer of 128 in between
    module = tf.keras.Sequential([tf.keras.layers.Flatten(input_shape=(28, 28)), tf.keras.layers.Dense(128, activation=tf.nn.relu), tf.keras.layers.Dense(10, activation=tf.nn.softmax)])

    # setup for compilation of the model, utilizing the Adam optimzer, 
    # and attempting to mimize with loss of sparse_categorical_crossentropy
    module.compile(optimizer=tf.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # training of data and labels using and epoch of 4 "4 loops essentially"
    module.fit(trainData, trainLabels, epochs=4)
    return module

def imageGray(img):
    # reads image using cv2 library and converts to grayscale if not already in it
    numImage = cv2.imread(img)
    greyConversion = cv2.cvtColor(numImage, cv2.COLOR_BGR2GRAY)
    return greyConversion


def readNums(g):
    # turns image into a binary image and find the curve "contour" that numbers are made with
    unused, th1 = cv2.threshold(g, 127, 255, cv2.THRESH_BINARY_INV)
    contours, h = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    final = []
    for i in contours:
        # assigns bounding rectangle for each letter found
        x,y,w,h = cv2.boundingRect(i)

        # obtains top right and bottom left corner of the digit being analyzed
        firstCorner = (x,y)
        secondCorner = (x+w, y+h)

        # cuts digit from background from top of height to bottom, then from far left width to right
        digit = th1[firstCorner[1]:secondCorner[1], firstCorner[0]:secondCorner[0]]
        # converts pixels to float for the new binary cut image 
        digit = digit/255

        # resizes to more closely resemable test case digits with 5 pixel whitespace border
        resizeToImage = cv2.resize(digit, (18,18))
        extraPadding = np.pad(resizeToImage, ((5,5),(5,5)), "constant", constant_values=0)
        final.append(extraPadding)
    return final

