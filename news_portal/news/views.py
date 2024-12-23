from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, PostCategory, Category, Comment
from sign.models import Author
from .forms import PostForm
from .filters import PostFilter
from .tasks import notify_new_post
from django.conf import settings


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = []
        for obj in PostCategory.objects.filter(post_id=context['object'].id):
            categories.append(Category.objects.get(id=obj.category_id).name)

        context['categories'] = categories
        context['user_id'] = self.request.user.id
        context['comments'] = Comment.objects.filter(post_id=context['object'].id)
        return context

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Редактирование публикации
    """
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование публикации"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'action': 'edit_post'})
        return kwargs


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Удаление публикации
    """
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('user_account')


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление новой публикации"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'action': 'create_post', 'user_id': self.request.user.id})
        return kwargs

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = Author.objects.get(user_id=self.request.user.id)

        # В зависимости от вызываемого url, подменяем тип публикации
        # Если articles/create/ - Статья (этот тип стоит по умолчанию в модели)
        # Если news/create/ - меняем тип на Новость
        if str(self.request).__contains__('news/create'):
            object.type_post = 'News'
        object.save()

        # Обновляем категории публикации
        for category_id in dict(self.request.POST)['category']:
            PostCategory.objects.create(category_id=category_id, post_id=Post.objects.last().pk)

        if settings.EMAIL_NEWSLETTER:
            notify_new_post.apply_async([object.pk], countdown=5)
        return HttpResponseRedirect('/sign/user_account')


class CommentDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Удаление комментария
    """
    permission_required = ('news.delete_comment',)
    model = Comment
    template_name = 'one_news.html'

    def post(self, request, *args, **kwargs):
        Comment.objects.get(id=kwargs["pk"]).delete()
        return redirect(f"/news/{request.POST.get('id_post', None)}")


class CommentCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Создание комментария
    """
    permission_required = ('news.add_comment',)
    model = Comment
    template_name = 'one_news.html'

    def post(self, request, *args, **kwargs):
        text = request.POST.get('text', None)
        id_post = request.POST['id_post']
        if text:
            Comment.objects.create(post=Post.objects.get(id=id_post),
                                   user=request.user,
                                   author=Author.objects.get(user_id=request.user.id),
                                   text=text,
                                   )

        return redirect(f"/news/{id_post}")
