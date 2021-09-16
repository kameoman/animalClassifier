from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import numpy as np

classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50

# モデルの作成
def main(X,y):
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

def model_train():
  model = Sequential()
  model.add(Conv2D(32,(3,3), padding='same',input_shape=X_train.shape[1:]))
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

  # 最適化
  opt = keras.optimizers.rmsprop(lr=0.001, decay=1e-6)

  # 正解と推定値がどれだけ離れているかを確認する
  model.compile(loss='categorical_crossentropy',
                optimaizer=opt,metrics=['accuracy'])

  # モデル作成のテスト回数
  model.fit(X, y, batch_size=32, nb_epoch=100)

  # モデル（分類器）の保存
  model.save('./animal_cnn.h5')

  return model

def model_eval(model,X, y):
  scores = model.evaluate(X, y, verbose=1)
  print('Test Loss:', scores[0])
  print('Test Accuracy:', scores[1])

if __name__ == "__main__":
  main()