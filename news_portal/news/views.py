from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post
from sign.models import Author
from .forms import PostForm
from .filters import PostFilter


# Create your views here.
class PostList(LoginRequiredMixin, ListView):
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
        context['user_id'] = self.request.user.id
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    """
    Показывает 1 статью
    """
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'post'


class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Редактирование публикации
    """
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Удаление публикации
    """
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CreatePost(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = Author.objects.get(user_id=self.request.user.id)

        # В зависимости от вызываемого url, подменяем тип публикации
        # Если articles/create/ - Статья (этот тип стоит по умолчанию в модели)
        # Если news/create/ - меняем тип на Новость
        if str(self.request).__contains__('news/create'):
            object.type_post = 'News'

        object.save()
        return HttpResponseRedirect('/sign/user_account')
