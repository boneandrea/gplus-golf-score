from datetime import date
import os
import sys
from jinja2 import Environment, FileSystemLoader
from total import *
from hdcp import *

args = sys.argv
verbose = False
if len(args) > 1:
    if args[1] == "-v":
        verbose = True

# 1. テンプレートファイルの場所と、レンダリング時のtrim設定を行う。
#    Environmentクラスはjinja2の中心的なクラスで、以下のように
#    設定を元にTemplateインスタンスを生成する役割を担う。
env = Environment(
    loader=FileSystemLoader('templates'),
    trim_blocks=True
)


def update_hdcp(template):
    hdcp_handler = hdcp()
    hdcp_handler.update_html(template)


template_hdcp = env.get_template('hdcp.html')
update_hdcp(template_hdcp)

# 2. テンプレートファイルを取得しレンダリングする。
#    レンダリング結果はファイルに出力する。
template = env.get_template('index.html')

x = total(verbose)
data = x.create_html_data()
prizes = x.count_prizes()
players = x.merge_prizes(data["result"], prizes)

year = date.today().year
result = template.render(
    title=f"ランキング: 水曜ゴルフGP {year}",
    msg="",
    year=year,
    data=players,
    bestscore=data["bestscore"]
)

dir = "docs/%s" % year

if os.path.isdir(dir):
    pass
else:
    os.mkdir(dir)

path = "%s/index.html" % dir

with open(path, 'w') as f:
    f.write(result)
