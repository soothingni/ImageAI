from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length=10, primary_key=True)     #캐릭터필드/PK 지정
    name = models.CharField(max_length=10)
    age = models.IntegerField()      #숫자필드
    hobby = models.CharField(max_length=20)

    def __str__(self):      #print를 했을 때 출력될 문자열 정의
        return self.userid + "/" + self.name