from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'type_post',
            'text',
            'category',
        ]
        labels = {
            'title': 'Наименование',
            'author': 'Автор',
            'type_post': 'Тип публикации',
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
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data