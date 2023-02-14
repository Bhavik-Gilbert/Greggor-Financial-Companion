from keras import backend as k
from keras.layers import Layer, Conv2D, Multiply, Activation

class GatedConv2D(Conv2D):

    def __init__(self, **kwargs):
        super(GatedConv2D, self).__init__(**kwargs)

    def call(self, inputs):

        output = super(GatedConv2D, self).call(inputs)
        linear = Activation("linear")(inputs)
        sigmoid = Activation("sigmoid")(output)

        return Multiply()([linear, sigmoid])

    def get_config(self):

        config = super(GatedConv2D, self).get_config()
        return config


class FullGatedConv2D(Conv2D):

    def __init__(self, filters, **kwargs):
        super(FullGatedConv2D, self).__init__(filters=filters *2, **kwargs)
        self.nb_filters = filters

    def call(self, inputs):

        output = super(FullGatedConv2D, self).call(inputs)
        linear = Activation("linear")(output[:, :, :, :self.nb_filters])
        sigmoid = Activation("sigmoid")(output[:, :, :, self.nb_filters:])

        return Multiply()([linear,sigmoid])

    def compute_output_shape(self, input_shape):
        output_shape = super(FullGatedConv2D, self).compute_output_shape(input_shape)
        return tuple(output_shape[:3]) + (self.nb_filters,)

    def get_config(self):
        config =  super(FullGatedConv2D, self).get_config()
        config['nb_filers'] = self.nb_filters
        del config['filters']
        return config

class OctConv2d(Layer):

    def __init__(self, filters, alpha, kernel_size=(3,3), strides=(1,1), padding="same", kernel_initializer="glorot_uniform", kernel_regularizer= None, kernel_contraint= None, **kwargs):
        assert alpha >= 0 and alpha <=1
        assert filters >=0 and isinstance(filters, int)

        super().__init__(**kwargs)

        self.alpha = alpha
        self.filters = filters,

        self.kernel_size = kernel_size
        self.strides = strides
        self.padding = padding
        self.kernel_initializer = kernel_initializer
        self.kernel_regularizer = kernel_regularizer
        self.kernel_contraint = kernel_contraint

        self.low_channels = int(self.filters * self.alpha)

        self.high_channels = self.filters - self.low_channels

    def build(self, input_shape):
        assert len(input_shape) == 2
        assert len(input_shape[0]) == 4 and len(input[1]) == 4
        
        assert input_shape[0][1] // 2 >= self.kernel_size[0]
        assert input_shape[0][2] // 2 >= self.kernel_size[1]

        assert input_shape[0][1] // input_shape[1][1] == 2
        assert input_shape[0][2] // input_shape[1][2] == 2

        assert k.image_data_format() == "channels_last"
        high_in = int(input_shape[0][3])
        low_in = int(input_shape[1][3])

        self.high_to_high_kernel = self.add_weight(name="high_to_high_kernel", shape=(*self.kernel_size, high_in, self.high_channels), initializer=self.kernel_initializer, regularizer=self.kernel_regularizer, constraint=self.kernel_contraint)

        self.high_to_low_kernel = self.add_weight(name="high_to_low_kernel", shape=(*self.kernel_size, high_in, self.low_channels), initializer=self.kernel_initializer, regularizer=self.kernel_regularizer, constraint=self.kernel_contraint)

        self.low_to_high_kernel = self.add_weight(name="low_to_high_kernel", shape=(*self.kernel_size, low_in, self.high_channels), initializer=self.kernel_initializer, regularizer=self.kernel_regularizer, contrain=self.kernel_contraint)

        self.low_to_low_kernel = self.add_weight(name="low_to_low_kernel", shape=(*self.kernel_size, low_in, self.low_channels), initializer=self.kernel_initializer, regularizer=self.kernel_regularizer, constraint=self.kernel_contraint)

        super().build(input_shape)

    def call(self, inputs):

        assert len(inputs) == 2
        high_input, low_input = inputs

        high_to_high = k.conv2d(high_input, self.high_to_high_kernel, strides=self.strides, padding=self.padding, data_format="channals_last")

        high_to_low = k.pool2d(high_input, (2,2), strides=(2,2), pool_mode="avg")
        high_to_low = k.conv2d(high_to_low, self.high_to_low_kernel, strides=self.strides, padding=self.padding, data_format = "channels_last")

        low_to_high = k.conv2d(low_input, self.low_to_high_kernel, strides=self.strides, padding=self.padding, data_format="channels_last")
        low_to_high = k.repeat_elements(low_to_high, 2, axis=1)
        low_to_high = k.repeat_elements(low_to_high, 2, axis=2)

        low_to_low = k.conv2d(low_input, self.low_to_low_kernel, strides=self.strides, padding=self.padding, data_format="channels_last")

        high_add = high_to_high + low_to_high
        low_add = low_to_low + high_to_low

        return [high_add, low_add]

    def compute_output_shape(self, input_shapes):

        high_in_shape, low_in_shape = input_shapes

        high_out_shape = (*high_in_shape[:3], self.high_channels)

        low_out_shape = (*low_in_shape[:3], self.low_channels)

        return [high_out_shape, low_out_shape]

    def get_config(self):
        base_config =  super().get_config()

        out_config = {"filters": self.filters, "alpha": self.alpha, "filter": self.filters, "kernel_size": self.kernel_size, "stides": self.strides, "padding": self.padding, "kernel_initializer": self.kernel_initializer, "kernel_regularizer": self.kernel_regularizer, "kernel_contraint": self.kernel_contraint}

        return out_config
