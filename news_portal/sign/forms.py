from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms
from .models import Author


# Create your models here.
class BasicSignupForm(SignupForm):
    """
    Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth.
    """
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    patronymic = forms.CharField(label="Отчество", required=False)
    age = forms.IntegerField(label="Возраст", required=False)

    def save(self, request):
        """
        переопределяем метод save
        :param request:
        :return:
        """
        user = super(BasicSignupForm, self).save(request)

        # Добавляем нового пользователя в группу
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        # Добавляем в таблицу Автор
        Author.objects.create(user=user,
                              full_name=f"{self.cleaned_data.get('first_name')} "
                                        f"{self.cleaned_data.get('last_name')}"
                                        f"{self.cleaned_data.get('patronymic')}",
                              age=self.cleaned_data.get('age'),
                              email=self.cleaned_data.get('email'))
        return user
