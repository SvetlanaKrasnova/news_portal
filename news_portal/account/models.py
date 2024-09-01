from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Автор
    """
    full_name = models.CharField(max_length=255)
    rating = models.FloatField(default=0)  # Рейтинг автора
