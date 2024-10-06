from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.action = kwargs.pop('action', None)
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]
        labels = {
            'title': 'Наименование',
            'text': 'Текст',
            'category': 'Категория'
        }

    def clean(self):
        """
        По документации, переопределяем метод clean, для проверки данных
        :return:
        """
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        if str(title).strip().lower() == str(text).strip().lower():
            raise ValidationError("Описание не должно быть идентичным названию.")

        if self.action == 'create_post':
            posts = Post.objects.filter(author__user=self.user_id,
                                        publishing_date__gt=date.today()).count()
            if posts >= 3:
                raise ValidationError("Истек лимит создания побликаций за день. "
                                      "В день можно создавать до 3 постов включитель.")

        return cleaned_data
