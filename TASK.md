# tasks

必要な画面
- データ取り込み内容確認画面
- コンペデータ編集画面
  - ニアピン
  - 新ペリHDCP


## 当日の流れ
1. 全データ取得(Python)
2. 名前修正
3. HDCP,ニアピン入力
4. ベスグロなど、データ更新(total.py)
5. HTML更新(publish)

## コンペデータ編集画面
- ニアピン王（回数）-> 手打ち
- GPポイントランキング王 -> HDCPを手打ち


送信内容をdbに入れるのでサーバが必要になる  
Railwayとすると
- mongo + webAppが必要
- python/node
  - phpよりinstall簡単？
  - phpはtemplateにない
  - しかしDockerfile頑張れば可能かも


## データ取り込み内容確認画面

pythonで取ってきたデータを一覧する

## コンペデータ編集画面

### どんな画面？

- スコアカードそのまま = pythonで取ってきたデータ

### 入力する内容
- ニアピン
- 新ペリHDCP
  - **年齢の判断はここでやってもらう**
    - 順位も入力可能にする
  - ここでポイントを合算する


# todo
- 表示内容とってくる
- 送信したらDBに入る
