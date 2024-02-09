from jinja2 import Environment, FileSystemLoader
from total import *

# 1. テンプレートファイルの場所と、レンダリング時のtrim設定を行う。
#    Environmentクラスはjinja2の中心的なクラスで、以下のように
#    設定を元にTemplateインスタンスを生成する役割を担う。
env = Environment(
    loader=FileSystemLoader('templates'),
    trim_blocks=True
)

# 2. テンプレートファイルを取得しレンダリングする。
#    レンダリング結果はファイルに出力する。
template = env.get_template('index.html')
x = total()
_data=x.create_html_data()
prizes = x.count_prizes()
r=x.merge_prizes(_data["result"],prizes)
print(r)

result = template.render(
    title='ランキング:水曜ゴルフGP 2024',
    data=r,#_data["result"],
    bestscore=_data["bestscore"]
)
with open('docs/index.html', 'w') as f:
    f.write(result)
