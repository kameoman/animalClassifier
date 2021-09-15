from keras.models import Sequential
from keras.layers import Convolution2D, MaxPool2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import numpy as np

classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50

# モデルの作成
def main():
  x_train, x_test, y_train, y_test = np.load("./")