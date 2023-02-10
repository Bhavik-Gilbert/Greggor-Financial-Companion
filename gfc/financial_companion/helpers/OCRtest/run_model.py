import resnet_arch
import data_prep

from keras.layers.normalization import batch_normalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import AveragePooling2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.convolutional import ZeroPadding2D
from keras.layers.core import Activation
from keras.layers.core import Dense
from keras.layers import Flatten
from keras.layers import Input
from keras.layers import Model
from keras.layers import Add as add
from keras.regularizers import L2
from keras import backend as k
from keras.optimizers import sgd_experimental, Adam

from keras.datasets import mnist
from keras import preprocessing
import numpy as np
import cv2
from sklearn import LabelBinarizer


EPOCHS = 50
INIT_LR = 1e-1
BS = 128

opt =sgd_experimental(learning_rate = INIT_LR, decay= INIT_LR/EPOCHS)

model = resnet_arch.ResNet.build(32,32,1,len(le.classes_), (3,3,3), (64,64,128, 256), reg=0.0005)

model.complie(loss="categorical_crossentropy", optimizer = opt, metrics= ["accuracy"])

H = model.fit(data_prep.aug.flow(data_prep.))