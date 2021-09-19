from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.saving.save import load_model
from keras.utils import np_utils
import keras
import numpy as np
from PIL import Image

classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50

def build_model():
  model = Sequential()
  model.add(Conv2D(32,(3,3), padding='same',input_shape=(50,50,3)))
  # 正しいところのみを通す
  model.add(Activation('relu'))
  model.add(Conv2D(32,(3,3)))
  model.add(Activation('relu'))
  # 一番大きい値を取り出す(最大値を取り出し特徴を際立たせる)
  model.add(MaxPool2D(pool_size=(2,2)))
  # 25%を消してデータの方よりを減らす
  model.add(Dropout(0.25))

  model.add(Conv2D(64,(3,3), padding='same'))
  model.add(Activation('relu'))
  model.add(Conv2D(64,(3,3)))
  model.add(Activation('relu'))
    # 一番大きい値を取り出す(最大値を取り出し特徴を際立たせる)
  model.add(MaxPool2D(pool_size=(2,2)))
  # 25%を消してデータの方よりを減らす
  model.add(Dropout(0.25))

  # 1列に並べる
  model.add(Flatten())
  # 連結する
  model.add(Dense(512))
  model.add(Activation('relu'))
  model.add(Dropout(0.5))

  # 最後の出力をどうしたいか（3個に分けるため３）
  model.add(Dense(3))
  # 一致しているか確率を出力する。
  model.add(Activation('softmax'))
  
  opt = tensorflow.keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)

  model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])

  # モデル（分類器）のロード
  model= load_model('./animal_cnn_aug.h5')

  return model