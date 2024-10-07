# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from .models import Post, Category
#
#
# def send_mail(post: dict, to: list):
#     instance = post['instance']
#     html_content = render_to_string(
#         'notify_new_post_mail.html',
#         {
#             'post': instance,
#             'username': post['username'],
#             'link': f'{settings.SITE_URL}/news/{instance.pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=f'{instance.title} {instance.publishing_date.strftime("%Y-%M-%d")}',
#         body=instance.text[:20],
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=to,
#     )
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
#
#
# @receiver(post_save, sender=Post)
# def notify_new_post(sender, instance, created, **kwargs):
#     """
#     Отправка уведомления пользователям о новой публикации
#     :param sender:
#     :param instance:
#     :param created:
#     :param kwargs:
#     :return:
#     """
#     if created:
#         categories = Category.objects.all()
#         for cat in categories:
#             for user in cat.subscribers.all():
#                 send_mail(post={'instance': instance,
#                                 'username': user.username},
#                           to=[user.email])
