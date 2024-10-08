from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    """
    Автор
    """
    full_name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(default=0)  # Рейтинг автора
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name.title()

    def update_rating(self):
        """
        суммарный рейтинг
            каждой статьи автора умножается на 3
            всех комментариев автора
            всех комментариев к статьям автора
        """
        # Если у автора ещё нет комментариев и постов, то пишем "0", так как Sum вернет None
        if posts_rating := self.post_set.aggregate(result=Sum('rating')).get('result') is None:
            posts_rating = 0

        if comments_rating := self.user.comment_set.aggregate(result=Sum('rating')).get('result') is None:
            comments_rating = 0

        self.rating = posts_rating * 3 + comments_rating
        self.save()
