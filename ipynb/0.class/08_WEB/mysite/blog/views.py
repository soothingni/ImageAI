from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from blog.models import Post
from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import Form
from django.forms import CharField, Textarea, ValidationError

# Create your views here.

def index(request):
    return HttpResponse('ok')

def index2(request, name):
    return HttpResponse('ok ' + name)

def index3(request, pk):
    #p = Post.objects.get(pk=pk)
    p = get_object_or_404(Post, pk=pk)
    return HttpResponse('ok ' + p.title)

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

class PostView(View):    #get/post를 나누어서 처리하고 싶을 때 아예 class로 묶어버릴 수도 있다.

    def get(self, request):
        return render(request, 'blog/edit.html')

    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        username = request.session['username']
        user = User.objects.get(username=username)
        Post.objects.create(title=title, text=text, author=user)
        return redirect('list')

class LoginView(View):

    def get(self, request):                           #보통 get은
        return render(request, 'blog/login.html')     #render로 form을 띄우고,

    def post(self, request):                          #post는
        username = request.POST.get('username')       #redirect로 끝난다.
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user == None:
            return redirect('login')   #여기 쓴 건 경로가 아니라, urls에서 정의한 경로의 name이다.
        request.session['username'] = username
        return redirect('list')

def validator(value):
    if len(value) < 5: raise ValidationError('길이가 너무 짧아요')

class PostForm(Form):
    title = CharField(label='제목', max_length=20, validators=[validator])
    text = CharField(label="내용", widget=Textarea)


class PostEditView(View):
    def get(self, request, pk):    #글을 수정하는 것이기 때문에 글을 특정할 pk를 전달받아야한다.
        post = Post.objects.get(pk=pk)
        form = PostForm(initial={'title':post.title, 'text': post.text})
        return render(request, 'blog/edit.html', {'form': form, 'pk': pk})

    def post(self, request, pk):
        form = PostForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=pk)
            post.title = form['title'].value()
            post.text = form['text'].value()
            post.publish()
            return redirect('list')
        return render(request, 'blog/edit.html', {'form':form, 'pk':pk})