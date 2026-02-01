from django.shortcuts import render, get_object_or_404
from .models import Article, ArticleImage, ArticleBlock

def blog_view(request):
    """Vue pour la page blog/articles"""
    articles = Article.objects.filter(publie=True).order_by('-cree_le')
    return render(request, 'articles/blog.html', {'articles': articles})

def article_detail(request, slug):
    """Vue pour le détail d'un article"""
    article = get_object_or_404(Article, slug=slug, publie=True)
    images = article.images.all()
    blocks = article.blocks.all()
    
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'images': images,
        'blocks': blocks,
    })
