from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import Post
from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from . import forms
from . import models

# Create your views here.
def index(request):
    return HttpResponse('ok')

def index2(request, name):
    return HttpResponse('ok ' + name)


def index3(request, pk):
    # p = Post.objects.get(pk=pk)
    p = get_object_or_404(Post, pk=pk)
    return HttpResponse('ok ' + p.title)

"""
def list(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    data = Post.objects.all().filter(author=user)
    context = {"data": data, "username": username}
    return render(request, "blog/list.html", context)

def detail(request, pk):
    p = get_object_or_404(Post, pk=pk)
    username = request.session['username']
    context = {"d": p, "username": username}
    return render(request, 'blog/detail.html', context)
"""

class LoginView(View):
    def get(self, request):  # 보통 get은
        return render(request, 'blog/login.html')  # render로 form을 띄우고,

    def post(self, request):  # post는
        username = request.POST.get('username')  # redirect로 끝난다.
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user == None:
            return redirect('login')  # 여기 쓴 건 경로가 아니라, urls에서 정의한 경로의 name이다.
        request.session['username'] = username
        return redirect('list')


class PostEditView(View):
    def get(self, request, pk, mode):
        if mode == 'add':
            form = forms.PostForm()
        elif mode == 'list':
            username = request.session['username']
            user = User.objects.get(username=username)
            data = Post.objects.all().filter(author=user)
            context = {"data": data, "username": username}
            return render(request, "blog/list.html", context)
        elif mode == 'detail':
            p = get_object_or_404(Post, pk=pk)
            return render(request, 'blog/detail.html', {'d': p})
        elif mode == 'edit':
            post = get_object_or_404(models.Post, pk=pk)
            form = forms.PostForm(instance=post)
        else:
            return HttpResponse("error page")
        return render(request, 'blog/edit.html', {'form': form})

    def post(self, request, pk, mode):
        username = request.session['username']
        user = User.objects.get(username=username)
        if pk == 0:
            form = forms.PostForm(request.POST)
        else:
            post = get_object_or_404(Post, pk=pk)
            form = forms.PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            if pk == 0:
                post.author = user
                post.save()
            else:
                post.publish()
            return redirect('edit', 0, 'list')   #urls.py에 전달할 pk와 mode를 render 함수에 함께 전달해주어야 한다.
        return render(request, "blog/edit.html", {'form': form})
