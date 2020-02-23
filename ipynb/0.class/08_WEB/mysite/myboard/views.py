from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from . import forms
from . import models
from django.conf import settings
from django.core.paginator import Paginator
from django.db import connection

# Create your views here.

cursor = connection.cursor()

def photolist(request, username):
    SQL = f"""SELECT filename
        FROM myboard_image
        WHERE author_id = (SELECT id FROM auth_user WHERE username = '{username}')
        """
    cursor.execute(SQL)
    data = dictfetchall(cursor)
    context = {'datas': data, 'username': username}
    return render(request, 'myboard/photolist.html', context)

def upload(request):
    # static에 저장
    username = request.GET.get('username')
    file = request.GET.get('filename')
    filename = file._name
    fp = open(settings.BASE_DIR + f"/static/faces/{username}/" + filename, "wb")
    for chunk in file.chunks():
        fp.write(chunk)
    fp.close()

    # db에 저장
    sql = f"""SELECT id from auth_user where username='{username}'"""
    cursor.execute(sql)
    author_id = cursor.fetchone()[0]
    SQL = f"""
    INSERT INTO "main"."myboard_image"
    ("author_id", "filename")
    VALUES ({author_id}, '{filename}');
    """
    cursor.execute(SQL)
    return JsonResponse()

def dictfetchall(cursor):   #cursor는 execute 후, fecth 전의 cursor다
    desc = cursor.description
    return [
        dict(zip([element[0] for element in desc], row))
        for row in cursor.fetchall()
    ]

def listsql(request, category, page):
    username = request.session['username']
    SQL = """SELECT b.id, title, cnt, username, category
    FROM myboard_board b, auth_user u

    WHERE b.author_id = u.id
    AND username= "@username"
    AND category="@category"
    """
    SQL = SQL.replace('@username', username).replace('@category', category)
    cursor.execute(SQL)
    data = dictfetchall(cursor)
    sub = data[(page-1)*3: page*3]
    return render(request, 'myboard/list3.html', {"datas": sub})


def ajaxdel(request):   #게시물 지우기
    pk = request.GET.get("pk")
    board = models.Board.objects.get(pk=pk)
    title = board.title
    #board.delete()
    result = f'{title}을 성공적으로 삭제했습니다.'
    return JsonResponse({'error': 0, 'result': result})

def ajaxget(request):   #페이지를 요청했을 때 해당 페이지 데이터를 전부 가져오기
    page = request.GET.get('page', 1)
    print(request.GET)
    datas = models.Board.objects.all().filter(category = 'common')
    page = int(page)
    sub = datas[(page-1)*3 : page*3]
    datas = {"datas": [{'pk': x.pk, 'title': x.title, 'cnt': x.cnt} for x in sub]}
    return JsonResponse(datas)

class BoardView(View):
    def get(self, request, category, pk, mode):
        if mode == 'add':
            form = forms.BoardForm()
        elif mode == 'list':
            username = request.session['username']
            user = User.objects.get(username=username)
            datas = models.Board.objects.all().filter(category=category)
            page = request.GET.get('page', 1)
            p = Paginator(datas, 3)  # 페이지당 글 수
            sub = p.page(page)
            context = {"datas": sub, "category": category, "username": username}
            return render(request, "myboard/list.html", context)
        elif mode == 'detail':
            p = get_object_or_404(models.Board, pk=pk)
            p.cnt += 1
            p.save()
            return render(request, 'myboard/detail.html', {'d': p})
        elif mode == 'edit':
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(instance=post)
        else:
            return HttpResponse("error page")
        return render(request, 'myboard/upload.html', {'form': form})

    def post(self, request, category, pk, mode):
        username = request.session['username']
        user = User.objects.get(username=username)
        if pk == 0:
            form = forms.BoardForm(request.POST)
        else:
            post = get_object_or_404(models.Board, pk=pk)
            form = forms.BoardForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            if pk == 0:
                post.author = user
                post.category=category
                file = request.FILES.get('file1')
                if file != None:
                    filename = file._name
                    fp = open(settings.BASE_DIR + "/static/" + filename, "wb")
                    for chunk in file.chunks():
                        fp.write(chunk)
                    fp.close()
                    post.image = filename
            post.save()
            return redirect('myboard', category, 0, 'list')
        return render(request, "myboard/upload.html", {'form': form})





