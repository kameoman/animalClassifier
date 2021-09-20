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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            # エラー時は、ファイルをアップロードする画面へredirectする
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
          # 変な文字や危険な文字が無いかを判定
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <html><head>
    <meta charset="UTF-8">
    <title>ファイルをアップロードして判別する</title></head>
    <body>
    <h1>ファイルをアップロードして判別する</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''