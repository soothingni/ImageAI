from flask import Flask, render_template, request
from yolo import *

app = Flask(__name__)

listData = [
        {"id": 0, "img": "img1.jpg", "title": "오로라1"},
        {"id": 1, "img": "img2.jpg", "title": "오로라2"},
        {"id": 2, "img": "img3.jpg", "title": "오로라3"}
    ]


def goURL(msg, url):
    html = """
<script>
    alert("@msg");
    window.location.href = "@url";
</script>
        """
    html = html.replace("@msg", msg)
    html = html.replace("@url", url)
    return html

def detectFace(img):
    return img


@app.route('/')
def index():
    return render_template('home.html', title='my home page')

@app.route('/image')
def image():
    return render_template('image.html', listData = listData)

@app.route('/view')      #/view?id=0
def view():
    id = request.args.get("id")
    for data in listData:
        if data["id"] == id:
            idx = listData.index(data)
    return render_template('view.html', s = listData[idx])

@app.route('/fileUpload', methods = ['POST'])
def fileUpload():
    f = request.files["file1"]
    title = request.form.get("title")
    algorithm = request.form.get("algorithm")
    f.save('./static/' + f.filename)
    if algorithm == 0:
        processed = yolo3('./static/' + f.filename)

    elif algorithm == 1:
        processed = detectFace('./static/' + f.filename)

    cv.imwrite('./static/' + f.filename, processed)
    id = listData[-1]['id'] + 1
    listData.append({"id": id, "img": f.filename, "title": title})
    return goURL("업로드가 성공했습니다.", "/image")

@app.route('/deleteimage')  #/delete?id=0
def delete():
    del_id = request.args.get("id")
    for data in listData:
        if data['id'] == int(del_id): listData.remove(data)
    return goURL("자료를 삭제했습니다.", "/image")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
