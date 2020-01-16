from flask import Flask, escape, request
import pickle
import urllib.request
import cv2, numpy as np
import time
from matplotlib import pyplot as plt
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


app = Flask(__name__)

#set FLASK_APP=앱.py
#flask run
#with open('data.picle', 'wb') as f:    
#    db = pickle.load(f)
db = {}
id = 0

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/<name>', methods = ['GET', 'POST'])
def hello_name(name):
    return f"Hello {name}!"

@app.route('/users', methods = ['POST'])
def create_user():
    global id
    body = request.json   #Nonetype Error: POST할 내용을 json 형식으로 전달해야함
    print(body)
    body['id'] = id
    db[str(id)] = body
    with open('data.picle', 'wb') as f:    
        pickle.dump(db, f)
    id += 1
    return body

@app.route('/users/<id>', methods = ['GET', 'PUT', 'DELETE'])
def select_user(id):
    if id not in db:
        return {}, 404
    return db[id]

def delete_user(id):
    del db[id]
    with open('data.picle', 'wb') as f:    
        pickle.dump(db, f)
    return {}

def update_user(id):
    new_body = request.json
    db[id].update(new_body)
    return {}

@app.route('/hi', methods = ['POST'])
def hi():
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "아 그 친구 참 멋있던데~(발그레)"
                    }
                }
            ]
        }
    }

@app.route('/namecard', methods = ['POST'])
def namecard():
    body = request.json
    #print("payload >> ", body)
    #pprint(body)
    image_url = body['userRequest']['params']['media']['url']
    #image_resp = request.get(image_url)
    #print("==image_resp==")

    #if 'http://dn-m.talk.kakao.com' in image_url:
        #print('image url>' image_url)
    urllib.request.urlretrieve(image_url, "namecard.png")
    img = cv2.imread("namecard.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    height, width = img.shape[:2]

    try:
        #원본 이미지 꼭짓점 --> 컨투어와 어프록시메이트 이용해서 찾기
        _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

        cnts, _ = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #사각형 추출
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:   #사각형인지 확인
                c_index = cnts.index(c)

        approx = cv2.approxPolyDP(cnts[c_index], 0.02 * peri, True)
        pts1 = approx.astype('float32')  #원본 점

        #원본 이미지의 크기로 퍼스펙티브화하기: 원본 꼭짓점 간 거리를 구해야 함
        a, b, c, d = approx
        width = np.linalg.norm(np.array(a)-np.array(b))
        height = np.linalg.norm(np.array(b)-np.array(c))

        pts2 = np.float32([[width, 0], [0, 0], [0, height], [width, height]])   #목적지 점
        
        M = cv2.getPerspectiveTransform(pts1, pts2)   #매트릭스 생성
        img_result = cv2.warpPerspective(img, M, (int(width), int(height))) #퍼스펙티브화

        #글자 인식
        s = pytesseract.image_to_string(img_result)
    except:
        s = "명함 인식 실패했다. 다른 이미지로 보내봐."
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": s
                    }
                }
            ]
        }
    }