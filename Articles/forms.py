# forms.py
from django import forms
from tinymce.widgets import TinyMCE
from .models import Article

class ArticleForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        required=True,
    )

    class Meta:
        model = Article
        fields = ['title','image', 'content']

