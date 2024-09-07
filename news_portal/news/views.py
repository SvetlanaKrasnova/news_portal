from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostList(ListView):
    """
    Информация о всех публикациях
    """
    model = Post
    ordering = 'title'
    template_name = 'all_news.html'
    context_object_name = 'all_news'

class PostDetail(DetailView):
    """
    Показывает 1 статью
    """
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'one_news'