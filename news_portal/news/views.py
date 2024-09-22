from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from .models import Post
from .forms import PostForm
from .filters import PostFilter


# Create your views here.
class PostList(ListView):
    """
    Информация о всех публикациях
    """
    model = Post
    ordering = '-publishing_date'
    template_name = 'all_news.html'
    context_object_name = 'all_news'
    paginate_by = 10

    def get_queryset(self):
        """
        Переопределяем функцию получения списка публикаций
        :return:
        """
        queryset = super().get_queryset()
        self.filter_posts = PostFilter(self.request.GET, queryset)
        return self.filter_posts.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_posts'] = self.filter_posts
        return context


class PostDetail(DetailView):
    """
    Показывает 1 статью
    """
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'post'


class PostEdit(UpdateView):
    """
    Редактирование публикации
    """
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    """
    Удаление публикации
    """
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CreatePost(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        # Получаем данные из формы
        self.object = form.save()

        # В зависимости от вызываемого url, подменяем тип публикации
        # Если articles/create/ - Статья (этот тип стоит по умолчанию в модели)
        # Если news/create/ - меняем тип на Новость
        if str(self.request).__contains__('news/create'):
            self.object.type_post = 'News'

        self.object.save()
        return HttpResponseRedirect('/news/')
