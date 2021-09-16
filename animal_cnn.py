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
  X_train, X_test, y_train, y_test = np.load("./animal.npy")
  # データを256の範囲から、0~1に正規化し精度を上げる
  X_train = X_train.astype("float") / 256
  X_test = X_test.astype("float") / 256
  # 0と1で動物の種類を再度設定[0-1-0][1-0-0][0-0-1]にして動物を判定する
  y_train = np_utils.to_categorical(y_train, num_classes)
  y_test = np_utils.to_categorical(y_test, num_classes)

  # モデル（分類器）の作成
  model = model_train(X_train, y_train)
  # モデル（分類器）の評価（テストする）
  model_eval(model, X_test, y_test)