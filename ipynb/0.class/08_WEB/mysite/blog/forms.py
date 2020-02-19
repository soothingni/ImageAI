from django import forms
from blog.models import Post
from django.forms import ValidationError

def validator(value):
    if len(value) < 5: raise ValidationError('길이가 너무 짧아요')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']   #모델 데이터에서 가져올 필드를 지정한다.

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].validators = [validator]