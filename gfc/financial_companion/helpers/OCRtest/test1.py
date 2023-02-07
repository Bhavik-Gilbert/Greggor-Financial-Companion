from keras.datasets import mnist
from keras import preprocessing
import numpy as np
import cv2
from sklearn import LabelBinarizer

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

        image = np.array([int(x) for x in row[1:]], dtype="utf8")

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

