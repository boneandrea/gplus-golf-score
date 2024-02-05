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
# print(x.create_html_data())

result = template.render(
    title='ランキング:水曜ゴルフGP 2024',
    data=x.create_html_data()
)
with open('docs/index.html', 'w') as f:
    f.write(result)
