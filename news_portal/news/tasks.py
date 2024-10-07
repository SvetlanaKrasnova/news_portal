from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
from news.models import Post, Category


def send_mail(post: dict, to: list):
    html_content = render_to_string(
        'notify_new_post_mail.html',
        {
            'text': post["text"],
            'username': post['username'],
            'link': f'{settings.SITE_URL}/news/{post["pk"]}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{post["title"]} {post["publishing_date"]}',
        body=post["text"][:20],
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def notify_new_post(post_id):
    """
    Уведомление о новом посте подписчикам
    :param post_id:
    :return:
    """
    post = Post.objects.get(pk=post_id)
    categories = Category.objects.all()
    for cat in categories:
        for user in cat.subscribers.all():
            send_mail(post={'pk': post_id,
                            'title': post.title,
                            'text': post.text,
                            'publishing_date': post.publishing_date.strftime("%Y-%M-%d"),
                            'username': user.username},
                      to=[user.email])


@shared_task
def notify_week_posts():
    """
    Задача на рассылку постов за неделю подписчикам
    :return:
    """
    start_date = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(publishing_date__gte=start_date)
    for category in Category.objects.all():
        posts.filter(category__name=category.name)
        if not posts.count():
            return

        html_content = render_to_string(
            'notify_week_posts_mail.html',
            {
                'link_home': settings.SITE_URL,
                'link_filter': f'{settings.SITE_URL}/search/?category={category.id}'
                               f'&publishing_date__gt={start_date.strftime("%Y-%m-%d")}',
                'posts': posts.filter(category__name=category.name),
            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=category.subscribers.values_list('email', flat=True),
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()
