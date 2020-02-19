from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from . import forms
from . import models
from django.conf import settings

# Create your views here.
class BoardView(View):
    def get(self, request, category, pk, mode):
        if mode == 'add':
            form = forms.BoardForm()
        elif mode == 'list':
            username = request.session['username']
            user = User.objects.get(username=username)
            data = models.Board.objects.all().filter(category=category)
            context = {"data": data, "category": category, "username": username}
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
                filename = file._name
                fp = open(settings.BASE_DIR + "/static/" + filename, "wb")
                for chunk in file.chunks():
                    fp.write(chunk)
                fp.close()
                post.image = filename
            post.save()
            return redirect('myboard', category, 0, 'list')
        return render(request, "myboard/upload.html", {'form': form})

