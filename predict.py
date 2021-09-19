from keras.models import Sequential,load_model
from keras.layers import Conv2D, MaxPool2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.saving.save import load_model
from keras.utils import np_utils
import keras, sys
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
  
  opt = keras.optimizers.RMSprop(lr=0.0001, decay=1e-6)

  model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])

  # モデル（分類器）のロード
  model= load_model('./animal_cnn_aug.h5')

  return model

def main():
  # コマンドラインでの読み取り一の指定（python pridict.py filename)
  # 上記のfilenameがargv[1]になる
  image = Image.open(sys.argv[1])
  # 白黒の写真の場合もあるため3色へ変換する
  image = image.convert('RGB')
  image = image.resize((image_size,image_size))
  # 画像を数字の列として保存する
  data = np.asarray(image)
  X = []
  X.append(data)
  X = np.array(X)
  model = build_model

  # predictで予測結果を示す
  result = model.predict([X])[0]
  # 一番大きい推定値を出すargmaxを使用
  predicted = result.argmax()
  percentage = int(result[predicted]*100)
  print("{0}({1}%)".format(classes[predicted],percentage))

if __name__ == "__main__":
  main()