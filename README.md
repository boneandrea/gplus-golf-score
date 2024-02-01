# 算出するもの

- 年間平均グロス王
- 年間ベスグロ回数
- バーディ王
- ニアピン王（回数）-> 手打ち
- ポイントランキング王 -> HDCPを手打ち


# Pythonのヘッドレスブラウザ使用

pip install -r requirements.e2e.txt 
python headless.py

# MongoDBを使う

管理画面から以下のvalueを取る
- `MONGO_INITDB_ROOT_USERNAME`
- `MONGO_INITDB_ROOT_PASSWORD`

## 接続
```
mongosh monorail.proxy.rlwy.net:56751 -u $MONGO_INITDB_ROOT_USERNAME
```

```
test> use score
switched to db score
score> db.score.insertOne({fe:1, puga:2})
{
  acknowledged: true,
  insertedId: ObjectId('65baa8b398030d88e4a311b3')
}
score> db.score.find()
[ { _id: ObjectId('65baa8b398030d88e4a311b3'), fe: 1, puga: 2 } ]
score> db.score.drop()
true
score> db.score.find()

score>
```

## Programmable access
https://www.hopes.host/blog/php-mongodb

# Railsway.appの設定
`MongoDB -> Settings _> Source -> Source Image -> mongo` をbuild

## 困った
Railway上のWeb mongodb UIからデータを直すと、dateがstringになる
-> tool作る(lose)
