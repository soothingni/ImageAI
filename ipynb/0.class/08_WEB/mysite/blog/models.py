from django.db import models
from django.utils import timezone


# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)   #auth.User를 지울 때 해당 User가 작성한 Post도 지우도록 설정
    title = models.CharField(max_length=200)
    text = models.TextField()  # 글자수에 제한 없는 텍스트
    created_date = models.DateTimeField(
        default=timezone.now)  # 날짜와 시간
    published_date = models.DateTimeField(
        blank=True, null=True) #  필드가 폼에서 빈 채로 저장되는 것을 허용; blank는 어플리케이션 측면, null은 데이터베이스 측면에서의 빈값을 의미

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title