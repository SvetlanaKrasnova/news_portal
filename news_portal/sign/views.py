from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Post, Category, UserCategory


# Create your views here.
class PersonalAccount(LoginRequiredMixin, TemplateView):
    """
    Страница профиля (личный кабинет)
    """
    template_name = 'user_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['full_name'] = f'{self.request.user.first_name} {self.request.user.last_name}'
        context['all_news'] = Post.objects.filter(author__user=self.request.user.id)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()

        # Для отображения подписок пользователя
        context['user_subscribe'] = []
        user_subscribe = UserCategory.objects.filter(user_id=self.request.user.id)
        for obj in user_subscribe:
            context['user_subscribe'].append(Category.objects.get(id=obj.category_id))

        all_categories = Category.objects.all()
        context['categories'] = [category for category in all_categories if not category in context['user_subscribe']]

        return context

    def post(self, request, *args, **kwargs):
        # Подписаться на категорию
        subscribe = request.POST.get('subscribe', None)
        if subscribe:
            if not UserCategory.objects.filter(category_id=subscribe, user_id=self.request.user.id).exists():
                UserCategory.objects.create(category_id=subscribe,
                                            user_id=self.request.user.id)

        # Отписаться от категории
        unsubscribe = request.POST.get('unsubscribe', None)
        if unsubscribe:
            subscribe = UserCategory.objects.get(category_id=unsubscribe,
                                                 user_id=self.request.user.id)
            subscribe.delete()
        return redirect('/sign/user_account/')


@login_required
def upgrade_me(request):
    """
    Добавление прав на публикацию статей (а так же на редактирование и удаление своих статей)
    :param request:
    :return:
    """
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)

    return redirect('/sign/user_account/')
