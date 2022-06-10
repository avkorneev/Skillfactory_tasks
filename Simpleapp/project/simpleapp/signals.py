from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.core.mail import send_mail, EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string

from project.project import settings
from project.simpleapp.models import Catsubs
from project.simpleapp.views import PostAdd


@receiver(post_save, sender=PostAdd)
def notify_publication(sender, instance, created, **kwargs):
    if created:
        print('CREATED')
        html_content = render_to_string('post_mail.html',
                                        {'title': instance.post_name, 'post': instance.post_text,
                                         'link': f'{Site.objects.get_current().domain + instance.get_absolute_url()}'})

        maillist = []  # список получателей
        for user in Catsubs.objects.filter(catsubs_to_cat=instance.post_to_postcat):  # перебираем всех юзеров, подписанных на категорию
            maillist.append(User.objects.get(pk=user.catsubs_to_subs.id).email)  # и закидываем в получателей
        msg = EmailMultiAlternatives(
            subject=f'Новый пост на NewsPortal: {instance.post_name}',  # тема
            body='',  # тело напишу в html
            from_email=settings.DEFAULT_FROM_EMAIL,
            # здесь указываете почту, с которой будете отправлять (об этом попозже)
            to=maillist  # список получателей уже составлен
        )
        msg.attach_alternative(html_content, "text/html")  # прикладываем html
        msg.send()  # отправляем


