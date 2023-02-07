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
from keras.layers import Add
from keras.regularizers import L2
from keras import backend as k

class ResNet:
    @staticmethod
    def residual_module(data, k, stride, chanDim, red=False,
     reg=0.0001, bnEps=2e-5, bnMom=0.9):
        
        shortcut = data


        bn1 = batch_normalization(axis=chanDim, epsilon=bnEps, 
        momentum=bnMom)(data)
        act1 = Activation("relu")(bn1)
        conv1 = Conv2D(int(k* 0.25), (1,1), use_bias=False,
        kernel_regularizer=12(reg))(act1)

        

