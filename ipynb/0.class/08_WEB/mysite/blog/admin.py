from django.contrib import admin
from blog.models import Post    #import할 때에는 base directory 기준으로 경로를 써준다.

# Register your models here.
admin.site.register(Post)