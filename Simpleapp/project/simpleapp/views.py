from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView

from .models import Post, User, Author, Category, Postcat, Catsubs
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, Upgrade
from django.contrib.auth.models import Group
from django.conf import settings


class PostAdd(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_post')
    template_name = 'simpleapp/post_add.html'
    form_class = PostForm

    # def post(self, request, *args, **kwargs):   #старая версия post, потом перекинул почту в form_valid
    #     maillist = []
    #     for user in Catsubs.objects.filter(catsubs_to_cat = self.request.POST['post_to_postcat']):
    #         maillist.append(User.objects.get(pk = user.catsubs_to_subs.id).email)
    #     print(maillist)
    #     send_mail(
    #         subject=f'Новый пост на NewsPortal', #{Post.post_datetime("%Y-%M-%d")}
    #         # имя клиента и дата записи будут в теме для удобства
    #         message=f'Здравствуй, {self.request.user}! Новая статья в твоём любимом разделе!',  # сообщение с кратким описанием проблемы
    #         from_email='',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
    #         recipient_list=maillist  # здесь список получателей. Например, секретарь, сам врач и т. д.
    #     )
    #
    #     return redirect('make_appointment')

    def form_valid(self, form):
        max_posts = 3 #максимальное число постов в сутки
        now = datetime.now()
        day_ago = timedelta(-1)
        user = self.request.user
        form.instance.post_to_author = Author.objects.get(author_to_user = User.objects.get(pk=user.id))
        if Post.objects.filter(post_to_author = Author.objects.get(author_to_user = user.id)).filter(post_datetime__gte=day_ago + now).count() < max_posts: #если не превысили максимальное число постов
            self.object = form.save()
            html_content = render_to_string('post_mail.html',
                                            {'title': self.object.post_name, 'post': self.object.post_text,
                                             'link': self.request.build_absolute_uri(
                                                 f'{self.object.id}')})  # выводим html в письмо. build_absolute_uri - для ссылки на пост
            maillist = []  # список получателей
            for user in Catsubs.objects.filter(catsubs_to_cat=self.request.POST[
                'post_to_postcat']):  # перебираем всех юзеров, подписанных на категорию
                maillist.append(User.objects.get(pk=user.catsubs_to_subs.id).email)  # и закидываем в получателей
            msg = EmailMultiAlternatives(
                subject=f'Новый пост на NewsPortal: {self.object.post_name}',  # тема
                body='',  # тело напишу в html
                from_email=settings.DEFAULT_FROM_EMAIL,
                # здесь указываете почту, с которой будете отправлять (об этом попозже)
                to=maillist  # список получателей уже составлен
            )
            msg.attach_alternative(html_content, "text/html")  # прикладываем html
            msg.send()  # отправляем
            return redirect('/cabinet/myposts')
        else: #если превысили - ничего не сохранится, и уведомления не придут
            return redirect('/cabinet/myposts')



# class UpgradeAuthor(LoginRequiredMixin, CreateView):
#     template_name = 'sign/upgrade.html'
#     form_class = Upgrade
#     model = Author
#
#     def form_valid(self, form):
#         user = self.request.user
#         author_group = Group.objects.get(name='Author')
#         if not self.request.user.groups.filter(name='Author').exists():
#             author_group.user_set.add(user)
#             form.instance.author_to_user = User.objects.get(pk=self.request.user.id)
#             self.object = form.save()
#             return redirect('/cabinet')
#         else:
#             return redirect('/cabinet')


class PostSearch(ListView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())

        context['time_now'] = datetime.utcnow()

        context['hotpost'] = None
        return context


class PostList(ListView):
    model = Post
    ordering = '-post_datetime'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        context['hotpost'] = None
        return context




class PostDetail(DetailView):
    template_name = 'simpleapp/post_details.html'
    queryset = Post.objects.all()


class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'simpleapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/cabinet/myposts/'
    permission_required = ('simpleapp.delete_post')
    def has_permission(self): #переписал метод из Миксина
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms) and self.get_object().post_to_author.author_to_user.id == self.request.user.id #если второе равенство не выполнится, то есть, пост чужой - не пустит менять



class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'simpleapp/post_add.html'
    form_class = PostForm
    permission_required = ('simpleapp.change_post')

    def has_permission(self): #переписал метод из Миксина
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms) and self.get_object().post_to_author.author_to_user.id == self.request.user.id #если второе равенство не выполнится, то есть, пост чужой - не пустит менять

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)




