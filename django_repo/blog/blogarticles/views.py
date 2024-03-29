from django.shortcuts import render, get_object_or_404
from blogarticles.models import BlogArticles

# Create your views here.

def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, 'blogarticles/title.html', {'blogs': blogs})

def blog_article(request, article_id):
    # article = BlogArticles.objects.get(id=article_id)
    article = get_object_or_404(BlogArticles, id=article_id)
    return render(request, 'blogarticles/content.html', {'article': article})