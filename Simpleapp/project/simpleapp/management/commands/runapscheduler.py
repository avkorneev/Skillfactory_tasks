import logging

from allauth.utils import build_absolute_uri
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta

from ...models import Catsubs, Post, Category

logger = logging.getLogger(__name__)

current_site = Site.objects.get_current()


# наша задача по выводу текста на экран
def my_job():  # что тут происходит?

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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', hour=21, minute=18, second=10),  # когда запускать рассылку
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
