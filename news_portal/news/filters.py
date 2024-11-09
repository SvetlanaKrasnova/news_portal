from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateFilter, ChoiceFilter
from django.forms import Select, SelectMultiple, TextInput, DateInput
from .models import Post, Category


class PostFilter(FilterSet):
    author = CharFilter(
        field_name='author__full_name',
        label='Автор',
        lookup_expr='icontains',
        widget=TextInput(
            attrs={'type': 'text',
                   'class': "form-control",
                   'placeholder': "Введите поисковый запрос...",
                   'aria-label': "Введите поисковый запрос...",
                   'aria-describedby': "button-search",
                   },
        ),
    )

    category = ModelMultipleChoiceFilter(
        label='Поиск по категориям',
        queryset=Category.objects.all(),
        widget=SelectMultiple(
            attrs={"class": "form-control"},
        ),
    )

    typy_post = ChoiceFilter(
        field_name='type_post',
        label='Поиск по типу публикации',
        choices=Post.TYPE_POST,
        widget=Select(
            attrs={"class": "form-control"},
        ),
    )

    title = CharFilter(
        field_name='title',
        label='Наименовние',
        lookup_expr='icontains',
        widget=TextInput(
            attrs={'type': 'text',
                   'class': "form-control",
                   'placeholder': "Введите поисковый запрос...",
                   'aria-label': "Введите поисковый запрос...",
                   'aria-describedby': "button-search",
                   },
        ),
    )

    publishing_date__gt = DateFilter(
        field_name="publishing_date",
        label="От даты",
        lookup_expr='gt',
        widget=DateInput(
            attrs={'type': 'date',
                   'class': "form-control",
                   },
        ),
    )

    class Meta:
        model = Post
        fields = ['title',
                  'author',
                  'category',
                  'publishing_date__gt',
                  ]
