from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv('.env')

key = os.environ.get("key")
secret = os.environ.get("secret")
# 連続してAPIを使用するとエラーになる可能性があるため待ち時間を作る
wait_time = 1

# 保存フォルダの指定
animalname = sys.argv[1]
savedir = "./" + animalname

flickr = FlickrAPI(key,secret, format='parsed-json')
# ここに検索時のパラメーターを入れる
result = flickr.photos.search(
  text = animalname,
  per_page = 400,
  media = 'photos',
  sort = 'relevance',
  safe_search = 1,
  extras = 'url_q, licence'
)

photos = result['photos']
# pprint(photos)
for i, photo in enumerate(photos['photo']):
  url_q = photo['url_q']
  filepath = savedir + '/' + photo['id'] + '.jpg'
  # 重複が無いように確認が必要(存在時飛ばす)
  if os.path.exists(filepath): continue
  urlretrieve(url_q,filepath)
  # アクセスの連続でAPIのエラーを防ぐため待機時間を作る
  time.sleep(wait_time)
