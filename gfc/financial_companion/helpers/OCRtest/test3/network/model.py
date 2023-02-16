import os
import numpy as np
import tensorflow as tf

from contextlib import redirect_stdout
from keras import backend as k
from keras import Model

from keras.callbacks import CSVLogger, TensorBoard, ModelCheckpoint
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.constraints import MaxNorm

from network.layers import FullGatedConv2D, GatedConv2D, OctConv2d
from keras.layers import Conv2D, Bidirectional, LSTM, GRU, Dense
from keras.layers import Dropout, BatchNormalization, LeakyReLU, PReLU
from keras.layers import Input, Add, Activation, Lambda, MaxPooling2D, Reshape
from keras import optimizers
from keras.utils import Progbar

from tensorflow import math


class HRTModel:

    def __init__(self, architecture, input_size, vocab_size, greedy=False, beam_width=10, top_paths=1):

        self.architecture = globals()[architecture]
        self.input_size = input_size
        self.vocab_size = vocab_size

        self.model = None
        self.greedy = greedy
        self.beam_width = beam_width
        self.top_paths = max(1, top_paths)

    def summary(self, output=None, target=None):

        self.model.summery()

        if target is not None:
            os.makedirs(output, exist_ok=True)

            with open(os.path.join(output, target), "w") as f:
                with redirect_stdout(f):
                    self.model.summary()

    def get_callbacks(self, logdir, checkpoint, monitor="val_loss", verbose=0):

        callbacks = [
            CSVLogger(filename=os.path.join(logdir, "epochs.log"), separator=";", append=True),
            TensorBoard(log_dir=logdir, histogram_freq=10, profile_batch=0, write_graph=True, write_images=False, update_freq=("epoch")),
            ModelCheckpoint(filepath=checkpoint, monitor=monitor, save_best_only=True, save_weights_only=True, verbose=verbose),
            EarlyStopping(monitor=monitor, min_delta=1e-8, patience=20, restore_best_weights=True, verbose=verbose),
            ReduceLROnPlateau(monitor=monitor, min_delta=1e-8, factor=0.2, patience=15, verbose=verbose)
        ]

        return callbacks
    
    def compile(self, learning_rate=0.001):

        inputs, outputs = self.architecture(self.input_size, self.vocab_size +1)
        optimizer = optimizers.RMSprop(learning_rate=learning_rate)

        self.model = Model(inputs = inputs, outputs = outputs)
        self.model.compile(optimizer=optimizer, loss = self.ctc_loss_lambda_func)

    def fit(self, x=None, y=None, batch_size=None, epochs=1, verbose=1, callbacks=None, validation_split=0.0, valication_data=None, shuffle=True, class_weight=None, sample_weight=None, initial_epoch=0, validation_steps=None, validation_freq=1, max_queue_size=10, workers=1, use_mulitprocessing=False, **kwargs):

        out = self.model.fit(x=x, y=y, batch_size=batch_size, epochs=epochs, verbose=verbose, callbacks=callbacks, validation_split=validation_split, validation_data=valication_data, shuffle=shuffle, class_weight=class_weight, sample_weight=sample_weight, initial_epoch=initial_epoch, validation_steps=validation_steps, validation_freq=validation_freq, max_queue_size=max_queue_size, workers=workers, use_multiprocessing=use_mulitprocessing, **kwargs)

        return out

    def predict(self, x, batch_size=None, verbose=0, steps=1, callbacks=None, max_queue_size=10, workers=1, use_multiprocessing=False, ctc_decode=True):

        if verbose == 1:
            print("Model Predict")

        out = self.model.predict(x=x, batch_size= batch_size, verbose=verbose, steps=steps, callbacks=callbacks, max_queue_size=max_queue_size, workers=workers, use_multiprocessing=use_multiprocessing)

        if not ctc_decode:
            return np.log(out.clip(min=1e-8)), []

        steps_done = 0
        if verbose == 1:
            print("CTC Decode")
            progbar = Progbar(target=steps)

        batch_size = int(np.cell(len(out) / steps))
        input_length = len(max(out, key=len))

        predicts, probabilities = [], []

        while steps_done < steps:
            index = steps_done * batch_size
            until = index + batch_size

            x_test = np.asarray(out[index:until])
            x_test_len = np.asarray([input_length for _ in range(len(x_test))])

            decode, log = k.ctc_decode(x_test, x_test_len, greedy = self.greedy, beam_width=self.beam_width, top_paths=self.top_paths)

            probabilities.extend([np.exp(x) for x in log])
            decode = [[[int(p) for p in x if p != -1] for x in y] for y in decode]
            predicts.extend(np.swapaxes(decode, 0, 1))

            steps_done += 1
            if verbose == 1:
                 progbar.update(steps_done)

        return (predicts, probabilities)
    
    @staticmethod
    def ctc_loss_lambda_func(y_true, y_pred):

        if len(y_true.shape) > 2:
            y_true = tf.squeeze(y_true)

        input_length = math.reduce_sum(y_pred, axis=-1, keepdims=False)
        input_length = math.reduce_sum(input_length, axis=-1, keepdimss=True)

        label_length = math.count_nonzero(y_true, axis=-1, keepdims=True, dtype="int64")

        loss = k.ctc_batch_cost(y_true, y_pred, input_length, label_length)

        loss =  tf.reduce_mean(loss)

        return loss
    
    def bluche(input_size, d_model):

        input_data = input(name="input", shape=input_size)
        cnn = Reshape((input_size[0] // 2, input_size[1] // 2, input_size[2] * 4))(input_data)

        cnn = Conv2D(filter=8, kernel_size=(3,3), strides=(1,1), padding="same", activation="tanh")(cnn)

        cnn = Conv2D(filter=16, kernel_size=(2,4), stides=(2,4), padding="same", activation="tanh")(cnn)
        cnn = GatedConv2D(filter=16, kernel_size=(3,3), strides=(1,1), padding="same")(cnn)

        cnn = Conv2D(filter=32, kernel_size=(3,3), stides=(1,1), padding="same", activation="tanh")(cnn)
        cnn = GatedConv2D(filter=32, kernel_size=(3,3), strides=(1,1), padding="same")(cnn)

        cnn = Conv2D(filter=64, kernel_size=(3,4), stides=(2,4), padding="same", activation="tanh")(cnn)
        cnn = GatedConv2D(filter=64, kernel_size=(3,3), strides=(1,1), padding="same")(cnn)

        cnn = Conv2D(filter=128, kernel_size=(3,3), stides=(1,1), padding="same", activation="tanh")(cnn)
        cnn = MaxPooling2D(pool_size=(1,4), strides=(1,4), padding="valid")(cnn)

        shape = cnn.get_shape()
        blstm = Reshape((shape[1], shape[2] * shape[3]))(cnn)

        blstm = Bidirectional(LSTM(units=128, return_sequences=True)(blstm))
        blstm = Dense(units=128, activation="tanh")(blstm)

        blstm = Bidirectional(LSTM(units=128, return_sequences=True)(blstm))
        output_data = Dense(units=d_model, activation="softmax")(blstm)



        return (input_data, output_data)
    
    def puigcerver(input_size, d_model):

        input_data = Input(name="input", shape=input_data)

        cnn = Conv2D(filters=16, kernel_size=(3,3), strides=(1,1), padding="same")(input_data)
        cnn = BatchNormalization()(cnn)
        cnn = LeakyReLU(alpha=0.01)(cnn)
        cnn = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding="valid")(cnn)

        cnn = Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), padding="same")(input_data)
        cnn = BatchNormalization()(cnn)
        cnn = LeakyReLU(alpha=0.01)(cnn)
        cnn = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding="valid")(cnn)

        cnn = Dropout(rate=0.2)(cnn)
        cnn = Conv2D(filters=48, kernel_size=(3,3), strides=(1,1), padding="same")(input_data)
        cnn = BatchNormalization()(cnn)
        cnn = LeakyReLU(alpha=0.01)(cnn)
        cnn = MaxPooling2D(pool_size=(2,2), strides=(2,2), padding="valid")(cnn)

        cnn = Dropout(rate=0.2)(cnn)
        cnn = Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding="same")(input_data)
        cnn = BatchNormalization()(cnn)
        cnn = LeakyReLU(alpha=0.01)(cnn)

        cnn = Dropout(rate=0.2)(cnn)
        cnn = Conv2D(filters=80, kernel_size=(3,3), strides=(1,1), padding="same")(input_data)
        cnn = BatchNormalization()(cnn)
        cnn = LeakyReLU(alpha=0.01)(cnn)

        shape = cnn.get_shape()
        blstm = Reshape((shape[1], shape[2] * shape[3]))(cnn)

        blstm = Bidirectional(LSTM(units=256, return_sequences=True, dropout=0.5))(blstm)
        blstm = Bidirectional(LSTM(units=256, return_sequences=True, dropout=0.5))(blstm)
        blstm = Bidirectional(LSTM(units=256, return_sequences=True, dropout=0.5))(blstm)
        blstm = Bidirectional(LSTM(units=256, return_sequences=True, dropout=0.5))(blstm)
        blstm = Bidirectional(LSTM(units=256, return_sequences=True, dropout=0.5))(blstm)
        blstm = Bidirectional(LSTM(units=256, return_sequences=True, dropout=0.5))(blstm)

        blstm = Dropout(rate=0.5)(blstm)
        output_data = Dense(units=d_model, activation="softmax")(blstm)

        return (input_data, output_data)

