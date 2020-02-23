from django.db import models
from django.utils import timezone


# Create your models here.
class Board(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)   #auth.User를 지울 때 해당 User가 작성한 Post도 지우도록 설정
    title = models.CharField(max_length=200)
    text = models.TextField()  # 글자수에 제한 없는 텍스트
    created_date = models.DateTimeField(
        default=timezone.now)  # 날짜와 시간
    cnt = models.IntegerField(default=0)
    image = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=10, default='common')

    def __str__(self):
        return self.title