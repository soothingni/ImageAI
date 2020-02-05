from flask import Flask, request, jsonify
from flask import request
import urllib
from bs4 import BeautifulSoup

app = Flask(__name__)

def getWeather(city):
    url = 'https://search.naver.com/search.naver?query='
    url += urllib.parse.quote_plus(city + ' 날씨')
    bs = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    temp = bs.select("span.todaytemp")
    desc = bs.select("p.cast_txt")

    return {"temp": temp[0].text,  "desc": desc[0].text}
    
@app.route('/weather')
def weather():
    city = request.args.get("city")
    info = getWeather(city)
    return jsonify(info)

@app.route('/dialogflow', methods = ['POST', 'GET'])                 #이 부분을 추가해준다!
def dialogflow():
    res = {'fulfillmentText': 'Hello'}       #'fulfillmentText' 키는 DialogFlow에서 규정된 것; 바꿀 수 없다.
    return jsonify(res)


@app.route('/')
#데코레이터임; 데코레이터 아래에 정의된 함수 앞|뒤로 코드를 붙여준다.
def home():
    name = request.args.get('name') 
    item = request.args.get('item')
    #메인 주소 뒤에 파라미터 지정할 수 있다.
    #e.g. http://127.0.0.1:3000/?name=sujin&item=한글
    return "hello " + name + item

@app.route('/abc')
def abc():
    return "test"

@app.route('/welcome/<name>')
def welcome(name):
    return "welcome " + name


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000, debug = True)