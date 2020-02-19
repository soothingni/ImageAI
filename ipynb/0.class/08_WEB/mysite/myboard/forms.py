from django import forms
from . import models
from django.forms import ValidationError

def validator(value):
    if len(value) < 5: raise ValidationError('길이가 너무 짧아요')

class BoardForm(forms.ModelForm):
    class Meta:
        model = models.Board
        fields = ['title', 'text']
    def __init__(self, *args, **kwargs):
        super(BoardForm, self).__init__(*args, **kwargs)
        self.fields['title'].validators = [validator]