from django.db import models
from django.contrib.auth.models import User
from sign.models import Author
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name.title()

class Post(models.Model):
    """
    Статья
    """
    ARTICLES = 'Articles'
    NEWS = 'News'
    TYPE_POST = [
        (ARTICLES, 'Статья'),
        (NEWS, 'Новость')
    ]
    title = models.CharField(max_length=150)  # Наименование статьи (заголовок)
    publishing_date = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    text = models.TextField()  # Текст статьи
    category = models.ManyToManyField(Category, through='PostCategory')  # На какую тему статья
    type_post = models.CharField(max_length=10,
                                 choices=TYPE_POST,
                                 default=ARTICLES)  # Тип публикации
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь между «Автором» и «Статьей».
    rating = models.FloatField(default=0)  # Популярность статьи (рейтинг)

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self, length: int = 124):
        return self.text if self.text.__len__() < length else f'{self.text[:length]} ...'


class Comment(models.Model):
    """
    Комментарий к статье
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # К какой статье оставлен коммент
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Кто написал
    text = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)  # На сколько полезен комментарий

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
