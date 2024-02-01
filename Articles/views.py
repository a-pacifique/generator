# articles/views.py
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.db.models import Q
from django.http import HttpResponse

def home(request):
    # Fetch the first three articles
    articles = Article.objects.all()[:3]
    return render(request, 'home.html', {'articles': articles})

def contact_us(request):
    return render(request, 'contact_us.html')

def about_us(request):
    return render(request, 'about_us.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article

def article_detail(request, slug):
    article = Article.objects.get(slug=slug)

    # Get suggested articles (you may need to define your own logic here)
    suggested_articles = Article.objects.exclude(slug=slug).order_by('-pub_date')[:3]

    context = {
        'article': article,
        'suggested_articles': suggested_articles,
    }

    return render(request, 'article_detail.html', context)


def generate_fixed_pcode():
    # Replace this with your fixed Pcode
    return '12345'


def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('article_detail', slug=article.slug)  # Replace with your detail view
    else:
        form = ArticleForm()

    return render(request, 'create_article.html', {'form': form})



def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form, 'article': article})


def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    
    return render(request, 'c', {'article': article})


def ads_txt(request):
    content = "google.com, pub-1335840781247344, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")
