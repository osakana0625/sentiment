from bottle import route,run,template,request,static_file
from janome.tokenizer import Tokenizer
import os



dict_polarity = {}
with open('./sentimental.txt', 'r') as f:
    line = f.read()
    lines = line.split('\n')
    for i in range(len(lines)):
        line_components = lines[i].split(':')
        dict_polarity[line_components[0]] = line_components[3]

@route('/')
def bo():
    return template('index.html')

@route('/', method='POST')
def search():
    sentimental = request.forms.getunicode('senti')#フォーム作成,文字列受け取り
    t = Tokenizer()
    #形態素解析
    tokens = t.tokenize(sentimental)
    pol_val = 0
    for token in tokens:
        word = token.surface
        pos = token.part_of_speech.split(',')[0]
        if word in dict_polarity:
            pol_val = pol_val + float(dict_polarity[word])
    if pol_val > 0.3:#極性値の程度が0.3以下だった場合
        return 'ポジティブ:',sentimental
    elif pol_val < -0.3:
        return 'ネガティブ:',sentimental
    else:
        return 'ニュートラル:',sentimental
    return template(sentimental=sentimental)


run(host='localhost', port=8080, debug=True)


    