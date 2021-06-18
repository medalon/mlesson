from django import forms
from django.forms import fields, widgets
from .models import Comment


class EmailNewsForm(forms.Form):
    name = forms.CharField(max_length=25, label="Имя", widget=forms.TextInput(attrs={"class": "form-control"}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    comments = forms.CharField(required=False,
                                widget=forms.Textarea(attrs={"class": "form-control",
                                                                "rows": 5}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'txt')