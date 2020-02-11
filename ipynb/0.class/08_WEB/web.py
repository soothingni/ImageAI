def renderfile(file, data):
    html = open(file, 'rt', encoding = 'utf-8').read()
    for key in data:
        html = html.replace('@' + key, data[key])
    return html

data = {"title": "나의 홈페이지", "name": "이순신", "email": "^^"}

html = renderfile("template.txt", data)

print(html)