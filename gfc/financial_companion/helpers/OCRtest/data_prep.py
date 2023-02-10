from keras.datasets import mnist
from keras import preprocessing
import numpy as np
import cv2
from sklearn.preprocessing import LabelBinarizer

def load_mnist_dataset():

    ((trainData, trainLabels), (testData, testLabels)) = mnist.load_data()

    data = np.vstack([trainData, testData])

    labels = np.hstack([trainLabels, testLabels])

    return (data, labels)

def load_az_dataset(datasetPath):

    data = []

    labels = []

    for row in open(datasetPath): 
        
        row = row.split(",")

        label = int(row[0])

        image = np.array([int(x) for x in row[1:]], dtype="uint8")

        image = image.reshape((28,28))

        data.append(image)

        labels.append(label)

    data = np.array(data, dtype='float32')

    labels = np.array(labels, dtype="int")

    return (data, labels)


(digitsData, digitsLabels) = load_mnist_dataset()

(azData, azLabels) = load_az_dataset('Data/A_Z_Handwritten_Data.csv')

azLabels += 10

data = np.vstack([azData, digitsData])

labels = np.hstack([azLabels, digitsLabels])

data = [cv2.resize(image, (32, 32)) for image in data]
data = np.array(data, dtype='float32')

data = np.expand_dims(data, axis=-1)
data /= 255.0

le = LabelBinarizer()
labels = le.fit_transform(labels)

counts = labels.sum(axis=0)

classTotals = labels.sum(axis=0)
classWeight = {}

for i in range(0, len(classTotals)):
    classWeight[i] = classTotals.max() / classTotals[i]



aug = preprocessing.image.ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.05,
    width_shift_range=0.1,
    shear_range=0.15,
    horizontal_flip=False,
    fill_mode="nearest"
)


from keras.layers import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import AveragePooling2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.convolutional import ZeroPadding2D
from keras.layers.core import Activation
from keras.layers.core import Dense
from keras.layers import Flatten
from keras.layers import Input 
from keras import Model
from keras.layers import Add as add
from keras.regularizers import L2
from keras import backend as k
from keras.optimizers import SGD
from keras import regularizers


class ResNet:
    @staticmethod
    def residual_module(data, k, stride, chanDim, red=False,
     reg=0.0001, bnEps=2e-5, bnMom=0.9):
        
        shortcut = data


        bn1 = BatchNormalization(axis=chanDim, epsilon=bnEps, 
        momentum=bnMom)(data)
        act1 = Activation("relu")(bn1)
        conv1 = Conv2D(int(k* 0.25), (1,1), use_bias=False,
        kernel_regularizer=regularizers.l2(reg))(act1)
        conv1 = Conv2D(int(k * 0.25), (1,1), use_bias=False,
        kernel_regularizer=regularizers.l2(reg)(act1)
        )
        

        bn2 = BatchNormalization(axis=chanDim, epsilon=bnEps, 
        momentum = bnMom)(conv1)
        act2 = Activation("relu")(bn2)
        conv2 = Conv2D(int(k * 0.25), (3,3), use_bias=False,
        kernel_regularizer=regularizers.l2(reg)(act2)
        )

        bn3 = BatchNormalization(axis=chanDim, epsilon=bnEps, 
        momentum = bnMom)(conv2)
        act3 = Activation("relu")(bn3)
        conv3 = Conv2D(int(k), (1,1), use_bias=False,
        kernel_regularizer=regularizers.l2(reg)(act3)
        )

        if red:
            shortcut = Conv2D(k, (1,1), strides=stride,
            use_bias=False, kernel_regularizer=regularizers.l2(reg))(act1)
        
        x = add([conv3], shortcut)

        return x

    @staticmethod
    def build(width, height, depth, classes, stages, filters, 
        reg=0.0001, bnEps=2e-5, bnMom=0.9, dataset="cifar"):

        inputShape = (height, width, depth)
        chanDim = -1

        if k.image_data_format() == "channels_first":
            inputShape = (depth, height, width)
            chanDim = 1
        
        inputs = Input(shape=inputShape)
        x = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum=bnMom)(inputs)

        if dataset == "cifar":
            x = Conv2D(filters[0], (3,3), use_bias=False, padding="same", kernel_regularizer=regularizers.l2(reg))(x)

        elif dataset == "tiny_imagenet":

            x = Conv2D(filters[0], (5,5), use_bias=False, padding = "same", kernel_regularizer=regularizers.l2(reg))(x)

            x = BatchNormalization(axis=chanDim, epsilon = bnEps, momentum= bnMom)(x)

            x = Activation("relu")(x)

            x = ZeroPadding2D((1,1))(x)

            x = MaxPooling2D((3,3), strides=(2,2))(x)
        
        for i in range(0, len(stages)):

            stride = (1,1) if i == 0 else (2,2)

            x = ResNet.residual_module(x, filters[i+1], stride, chanDim, red =True, bnEps=bnEps, bnMom=bnMom)

            for j  in range(0, stages[i] -1):

                x = ResNet.residual_module(x, filters[i+1], stride, chanDim, red =True, bnEps=bnEps, bnMom=bnMom)

        x = BatchNormalization(axis=chanDim, epsilon=bnEps, momentum= bnMom)(x)

        x = Activation("relu")(x)
        X = AveragePooling2D((8,8))(x)

        x = Flatten()(x)
        x = Dense(classes, kernel_regularizer=regularizers.l2(reg))(x)
        x = Activation("softmax")(x)

        model = Model(inputs, name="resnet")

        return model



EPOCHS = 1
INIT_LR = 1e-1
BS = 128

opt = SGD(learning_rate = INIT_LR, decay= INIT_LR/EPOCHS)

model = ResNet.build(32,32,1,len(le.classes_), (3,3,3), (64,64,128, 256), reg=0.0005)

model.complie(loss="categorical_crossentropy", optimizer = opt, metrics= ["accuracy"])

H = model.fit(aug.flow(trainX, trainY, batch_size=BS), validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS, epochs=EPOCHS, class_weight= classWeight, verbose=1)