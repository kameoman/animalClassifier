import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
# 受け付けるアップロードデータの種類
ALLOWED_EXTENSIONS = set(['png','jpg','gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  # .があるか、また拡張子にjpgなどがあるかを判定する
  return '.'in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS