from PIL import Image
import os, glob
import numpy as np
from numpy.core.defchararray import array
from sklearn import model_selection

classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50
num_testdata = 75

# 画像を読み込んで扱いやすいように配列（数値等に変換）

x_train = []
x_test = []
Y_train = []
Y_test = []
for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob(photos_dir + "/*.jpg")
    for i, file in enumerate(files):
        if i >= 150: break
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size,image_size))
        data = np.asarray(image)

        if i < num_testdata:
            x_test.append(data)
            Y_test.append(index)
        else:
            x_train.append(data)
            Y_train.append(index)

            for angle in range(-20,20,5):
                # 画像を回転させてデータ量を増やす
                img_r = image.rotate(angle)
                data = np.asarray(img_r)
                x_train.append(data)
                Y_train.append(index)

                # 左右反転する
                img_trans = image.transpose(Image.FLIP_LEFT_RIGHT)
                data = np.asarray(img_trans)
                x_train.append(data)
                Y_train.append(index)
                

        # X.append(data)
        # Y.append(index)

# X = np.array(X)
# Y = np.array(Y)

X_train = np.array(x_train)
X_test = np.array(x_test)
y_train = np.array(Y_train)
y_test = np.array(Y_test)

# それぞれのデータをテストと学習に分けて保存する
# X_train, X_test, y_train, y_test = model_selection.train_test_split(X,Y)
xy = (X_train, X_test, y_train, y_test)
np.save("./animal_aug.npy",xy)