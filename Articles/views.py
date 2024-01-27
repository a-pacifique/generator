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
    article = get_object_or_404(Article, slug=slug)

    # Check if there is a next article
    try:
        next_article = Article.objects.filter(id__gt=article.id).order_by('id')[0]
    except IndexError:
        next_article = None

    # Check if the user clicked an ad
    ad_clicked = request.GET.get('ad_clicked', False)

    # Check if the current article is the last one (ID 11) and the ad is clicked
    is_last_article = article.id == 11 and ad_clicked

    return render(request, 'article_detail.html', {
        'article': article,
        'next_article': next_article,
        'ad_clicked': ad_clicked,
        'is_last_article': is_last_article,
    })


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


def task_completion(request):
    # Retrieve Job ID and Worker ID from the session
    job_id = request.session.get('job_id')
    worker_id = request.session.get('worker_id')

    # PCODE Secret Key
    secret_key = "c20eb93d2436604848f373635614d90ff1bd13987e3d2545aea4bee5f1e88b43"

    # Generate PCODE
    final_string = f"{job_id}{worker_id}{secret_key}"
    pcode = f"pw-{hashlib.sha256(final_string.encode()).hexdigest()}"

    # Display PCODE to the worker
    return HttpResponse(f"Worker, your PCODE is: {pcode}")

