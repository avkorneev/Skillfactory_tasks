from datetime import datetime, timedelta

from celery import shared_task
import time

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Catsubs, User, Post, Category, Postcat


@shared_task
def hello():
    print("Hello, world!")


@shared_task
def mail_post(post_id, *args, **kwargs):
    post = Post.objects.get(pk = post_id)
    html_content = render_to_string('post_mail.html',
                                    {'title': post.post_name, 'post': post.post_text,
                                     'link': f'{Site.objects.get_current().domain + post.get_absolute_url()}'}) #instance.request.build_absolute_uri(
                                         #f'{instance.object.id}')})  # выводим html в письмо. build_absolute_uri - для ссылки на пост
    maillist = []  # список получателей
    post_categories = []
    cat = Postcat.objects.filter(postcat_to_post = post).values_list('postcat_to_cat', flat=True)
    for user in Catsubs.objects.filter(catsubs_to_cat__in=cat):  # перебираем всех юзеров, подписанных на категорию
        maillist.append(User.objects.get(pk=user.catsubs_to_subs.id).email)  # и закидываем в получателей
    msg = EmailMultiAlternatives(
        subject=f'Новый пост на NewsPortal: {post.post_name}',  # тема
        body='',  # тело напишу в html
        from_email=settings.DEFAULT_FROM_EMAIL,
        # здесь указываете почту, с которой будете отправлять (об этом попозже)
        to=maillist  # список получателей уже составлен
    )
    msg.attach_alternative(html_content, "text/html")  # прикладываем html
    msg.send()  # отправляем


@shared_task
def weekly_mail():
    print('Hey')
    last_week = datetime.now() + timedelta(-7)  # выставили выдачу постов за последнюю неделю

    for user in User.objects.all():  # идём по всем юзерам
        post_list = Post.objects.none()  # каждому юзеру соответствует список постов, которые он получит на почту
        html_content = f'''<h1>Привет, {user}! Мы подвезли посты из твоих подписок за последнюю неделю!</h1><br>'''  # общее приветствие
        for sub in Catsubs.objects.filter(catsubs_to_subs=user):  # перебираем подписки юзера
            post_list = post_list | Post.objects.filter(post_to_postcat=sub.catsubs_to_cat).filter(
                post_datetime__gte=last_week)  # берём посты за последнюю неделю с той же категорией, что и в текущей
            # подписке
            # и объединяем с post_list
        for post in post_list.distinct():  # перебираем набранные посты, удалив дупликаты

            html_content += f'{post.post_name} by {post.post_to_author}<br>'  # в выдачу запихнули название поста и
            # автора
            html_content += f'{Site.objects.get_current().domain + post.get_absolute_url()}<br>'  # и ссылку на пост,
            # составленную костыльным методом без request. В domain name в админке надо указать
            # http://127.0.0.1:8000, либо актуальный домен

        if post_list:  # если список постов вышел пустой, ничего отправлять не будем

            maillist = [user.email]  # список получателей
            msg = EmailMultiAlternatives(
                subject=f'Ваши любимые посты на NewsPortal за последнюю неделю',  # тема
                body='',  # тело напишу в html
                from_email=settings.DEFAULT_FROM_EMAIL,
                # здесь указываете почту, с которой будете отправлять (об этом попозже)
                to=maillist  # список получателей уже составлен
            )
            msg.attach_alternative(html_content, "text/html")  # прикладываем html
            msg.send()  # отправляем
            # и идём к следующему юзеру