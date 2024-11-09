from datetime import date
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, CharField, ModelMultipleChoiceField, SelectMultiple
from django_summernote.widgets import SummernoteWidget
from .models import Post, Category


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.action = kwargs.pop('action', None)
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)

    title = CharField(
        label='Наименовние',
        widget=TextInput(
            attrs={'type': 'text',
                   'class': "form-control form_field_post",
                   'placeholder': "Наименование публикации",
                   },
        ),
    )

    text = CharField(
        label='Текст',
        widget=SummernoteWidget(
            attrs={'summernote': {'width': '1100px', 'height': '700px'}
                   },
        ),
    )
    category = ModelMultipleChoiceField(
        label="Категория",
        queryset=Category.objects.all(),
        widget=SelectMultiple(
            attrs={"class": "form-control form_field_category"},
        ),
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]

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
