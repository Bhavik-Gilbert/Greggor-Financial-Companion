import os
import numpy as np
import tensorflow as tf

from contextlib import redirect_stdout
from keras import backend as k
from keras import Model

from keras.callbacks import CSVLogger, TensorBoard, ModelCheckpoint
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.constraints import MaxNorm

from network.layers import FullCatedConv2d, GatedConv2D, OctConv2D
from keras.layers import Conv