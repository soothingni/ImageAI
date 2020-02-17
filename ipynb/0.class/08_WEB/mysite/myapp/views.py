from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from . import face
from myapp.models import User

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

def index(request):    #flask의 request 객체가 아니다!!!!!!!!
    return HttpResponse("Hello Django!!!")

def test(request):
    data = {"s": {"img":"test.png"}, "list": [1, 2, 3, 4, 5]}
    return render(request, 'template.html', data)

def login(request):
    id = request.GET.get("id")
    pwd = request.GET.get("pwd")
    if id == pwd:
        request.session['user'] = id

        return redirect("/service")    #service(requests)
    return redirect("/static/login.html")

def service(request):
    #로그인을 했는지 안했는지 확인
    if request.session.get("user", "") == "":
        return redirect("/static/login.html")
    html = "Main Service <br>" + request.session.get("user") + "님 감사합니다."
    return HttpResponse(html)

# def logout(request):
# #     request.session["session"] = ""
# #     request.session.pop("user")
# #     return redirect("/static/login.html")


@csrf_exempt
def uploadimage(req):
    file = req.FILES['file1']    #.FILES 안에 파일 타입 데이터를 다 저장하고 있다.
    filename = file._name
    print(filename)
    fp = open(settings.BASE_DIR + "/static/" + filename, "wb")
    for chunk in file.chunks():   #데이터가 클 수도 있기 때문에 chunk로 잘라서 가져온다.
        fp.write(chunk)
    fp.close()
    result = face.faceverification('known.bin', './static/' + filename)
    if result[0] != "Unknown":
        req.session['user'] = result[0]
        return redirect('/service')
    html = goURL("등록되지 않은 사용자입니다. 다시 시도해주세요.", "/static/login.html")
    return HttpResponse(html)


def listUser(request):
    if request.method == 'GET':  #GET 방식으로 요청이 들어왔을 경우
        q = request.GET.get('q', "")
        del_id = request.GET.get('userid', "")
        data = User.objects.all()
        if q != "":
            data = User.objects.all().filter(name__contains=q)
        elif del_id != "":
            data.get(userid=del_id).delete()   #get: filter랑 똑같은데, 결과가 1개 일때만 가능
            return redirect('/listuser')
        return render(request, 'template2.html', {"data": data})
    else:                      #POST 방식으로 요청이 들어왔을 경우
        u = User(userid=request.POST.get('userid'),
                 name=request.POST.get('name'),
                 age=request.POST.get('age'),
                 hobby=request.POST.get('hobby'))
        u.save()
        return redirect("/listuser")
