from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import sys
from io import StringIO
# Create your views here.

def index(request):
    return HttpResponse("hello ajax")


def calcForm(request):
    return render(request, "ajax/calc.html")   #템플릿은 디폴트 루트가 templates 폴더다; => templates > ajax > cacl.html을 읽어오라는 뜻


def calc(request):
    op1 = int(request.GET['op1'])
    op2 = int(request.GET['op2'])
    result = op1 + op2
    # return HttpResponse("{'result': str(result) + }")
    return JsonResponse({'error': 0, 'result': result})    #딕셔너리를 json으로 바꿔주는 함수

def loginform(request):
    return render(request, "ajax/login.html")

def login(request):
    id = request.GET.get("id")
    pwd = request.GET.get("pwd")
    if id == pwd:
        request.session['user'] = id
        return JsonResponse({'error': 0, 'message': "로그인 성공"})
    return JsonResponse({'error': -1, 'message': 'id/pwd를 확인해주세요.'})

def uploadform(request):
    return render(request, "ajax/upload.html")

def upload(request):
    file = request.FILES['file1']
    filename = file._name
    fp = open(settings.BASE_DIR + "/static/" + filename, "wb")
    for chunk in file.chunks():
        fp.write(chunk)
    fp.close()
    return HttpResponse("업로드 성공")

def runpythonForm(request):
    return render(request, 'ajax/runpython.html')

glo = {}
loc = {}

def runpython(request):
    code = request.GET.get('code')
    original_stdout = sys.stdout
    sys.stdout = StringIO()  # 원래는 모니터로 가던 출력값을 메모리로 가로채도록
    exec(code, glo, loc)
    contents = sys.stdout.getvalue()  # 메모리로 가로챈 출력값을 `contents` 변수에 저장
    contents = contents.replace("\n", "<br>")
    sys.stdout = original_stdout
    return HttpResponse(contents)