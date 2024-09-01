from django.db import models
from account.models import Author


# Create your models here.
class News(models.Model):
    """
    Статья
    """
    development = 'IT'
    sd = 'SD'
    marketing = 'Marketing'
    management = 'Management'
    scientific = 'Science'

    TOPIC = [
        (development, 'Разработка'),
        (sd, 'Администрирование'),
        (marketing, 'Маркетинг'),
        (management, 'Менеджмент'),
        (scientific, 'Научная')
    ]
    name = models.CharField(max_length=255)  # Наименование статьи
    publishing_date = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    description = models.TextField(default="Описание не указано")  # Текст статьи
    topic = models.CharField(max_length=10,
                             choices=TOPIC,
                             default=sd)  # На какую тему статья
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь между «Автором» и «Статьей».
    rating = models.FloatField(default=0)  # Популярность статьи (рейтинг)


class Comment(models.Model):
    """
    Комментарий к статье
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE) # К какой статье оставлен коммент
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # Кто написал
    text = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0) # На сколько полезен комментарий
