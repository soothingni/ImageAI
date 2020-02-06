from flask import Flask, request, jsonify
from flask import request
import urllib
from bs4 import BeautifulSoup
import json

cnt = 0

def getQuery(word):
    url = 'https://search.naver.com/search.naver?where=kdic&query='
    url += urllib.parse.quote_plus(word)
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

    output = bs.select('p.txt_box')
    #return a[0].text
    return [node.text for node in output] 

def getWeather(city):
    url = 'https://search.naver.com/search.naver?query='
    url += urllib.parse.quote_plus(city + ' 날씨')
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    temp = bs.select("span.todaytemp")
    desc = bs.select("p.cast_txt")

    return {"temp": temp[0].text,  "desc": desc[0].text}

app = Flask(__name__)

@app.route('/')
def home():
    html = """<iframe 
    id="frame" 
    class="b_frame" 
    allow="microphone;"
    width = "300"
    height = "500"
    src="https://console.dialogflow.com/api-client/demo/embedded/aichatbot_8895">
    </iframe>"""
    return html

@app.route('/counter')
def counter():
    global cnt
    cnt += 1
    files = [f"{digit}.jpg" for digit in str(cnt)]
    return_str = " ".join([f"<img src=/static/{file}?12>" for file in files])
    return f"{return_str}명이 방문했습니다."

@app.route('/weather', methods = ['POST', 'GET'])
def weather():
#     if request.method == "POST":
#         req = request.form
#     else:
#         req = request.args
    
    req = request.form if request.method == "POST" else request.args
    
    city = req.get("city")
    
    return f"{city} 날씨 좋아요"

@app.route('/dialogflow', methods = ['POST', 'GET'])
def dialogflow():
    req = request.get_json(force=True)
    print(json.dumps(req, indent = 4, ensure_ascii = False))
    
    answer = req['queryResult']['fulfillmentText']
    intentName = req['queryResult']['intent']['displayName']
    
    if intentName == 'Query':
        word = req['queryResult']['parameters']['any']
        answer = getQuery(word)[0]
    
    elif intentName == 'Order2':
            price = {'짜장면': 5000, '짬뽕': 10000, '탕수육': 20000}
            params = req['queryResult']['parameters']['food_number']

            output = [food.get("number-integer", 1) * price[food['food']] for food in params]
            #get을 쓰는 이유는 음식이 하나인 경우 수량을 명시하지 않는 경우도 있기 때문(에러핸들링의 측면에서)
            answer = f"총 {int(sum(output))}원입니다."

    elif intentName == 'Weather' and req['queryResult']['allRequiredParamsPresent'] == 1:
        date = req['queryResult']['parameters']['date']
        geo_city = req['queryResult']['parameters']['geo-city']
        
        info = getWeather(geo_city)
        
        answer = f"{geo_city} 날씨 정보 : {info['temp']} / {info['desc']}"
                 
    res = {'fulfillmentText': answer}
        
    return jsonify(res)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000, debug = True)