from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from news.models import Post


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
        return context


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
