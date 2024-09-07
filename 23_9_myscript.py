import json
import random
from datetime import datetime
from django.contrib.auth.models import User
from account.models import Author
from news.models import Category, Post, Comment

# 1. Создать 2 пользователей
guest_user_1 = User.objects.create_user('skrasnova')
guest_user_2 = User.objects.create_user('ivanovivan')

# 2. Создать 2 объекта модели Author, связанные с пользователями.
author_1 = Author.objects.create(user=guest_user_1,
                                 full_name='Краснова Светлана Анатольевна',
                                 email='test_1@yandex.ru')
author_2 = Author.objects.create(user=guest_user_2,
                                 full_name='Иванов Иван Иванович',
                                 email='i_ivanov_19@mail.ru',
                                 age=39)

# 3. Добавить 4 категории в модель Category
for name in ['Разработка', 'Менеджмент', 'Наука', 'IT']:
    Category.objects.create(name=name)

# 4. Добавить 2 статьи и 1 новость.
with open('data.json', 'r', encoding='utf-8') as file: data = json.load(file)

all_news = []
for el in data["papers"]:
    post = Post.objects.create(title=el["title"],
                               publishing_date=datetime.now(),
                               text=el["text"],
                               # category=el["category"],
                               type_post=Post.paper,
                               author=author_1)
    all_news.append(post)

news = data["news"]
all_news.append(Post.objects.create(title=news["title"],
                                    publishing_date=datetime.now(),
                                    text=news["text"],
                                    # category=el["category"],
                                    type_post=Post.news,
                                    author=author_2))

# 5 Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
all_news[0].category.add(Category.objects.get(id=1), Category.objects.get(id=4))
all_news[1].category.add(Category.objects.get(id=1))
all_news[2].category.add(Category.objects.get(id=2))

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
for post in all_news:
    for number in range(5):
        text = f"{post.author.user.username} {random.choice(data['comments'])}"
        Comment.objects.create(post=post, user=post.author.user, author=post.author, text=text)

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
for post in all_news:
    random.choice([post.like, post.dislike, post.like])()

for comment in Comment.objects.all():
    random.choice([comment.like, comment.dislike, comment.like])()

# 8. Обновить рейтинги пользователей.
for author in Author.objects.all():
    author.update_rating()

for author in Author.objects.all():
    print(author.rating)
# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
author = Author.objects.order_by('-rating').first()
print(f"\nАвтор с самым высоким рейтингом:"
      f"\nusername: {author.user.username}"
      f"\nrating: {author.rating}")

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье.
post = Post.objects.order_by('-rating').first()
print("\n\nСтатья с самым высоким рейтингом")
print(f"\nДата добавления: {post.publishing_date}"
      f"\nАвтор: {post.author.user.username}"
      f"\nРейтинг статьи: {post.rating}"
      f"\nЗаголовок: {post.title}"
      f"\nПревью: {post.preview()}")

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
print("\n\nКомментарии к статье")
for comment in post.comment_set.values('date_time', 'author', 'rating', 'text'):
    print(f"\nДата добавления: {comment['date_time']}"
          f"\nАвтор: {comment['author']} {comment['text'].split(' ')[0]}"
          f"\nРейтинг: {comment['rating']}"
          f"\nТекст: {comment['text']}")
