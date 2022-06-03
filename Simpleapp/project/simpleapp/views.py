from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView

from .models import Post, User, Author
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, Upgrade
from django.contrib.auth.models import Group
from django.conf import settings


class PostAdd(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_post')
    template_name = 'simpleapp/post_add.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.post_to_author = Author.objects.get(author_to_user = User.objects.get(pk=self.request.user.id))
        self.object = form.save()
        return redirect('/cabinet')


class UpgradeAuthor(LoginRequiredMixin, CreateView):
    template_name = 'sign/upgrade.html'
    form_class = Upgrade
    model = Author

    def form_valid(self, form):
        user = self.request.user
        author_group = Group.objects.get(name='Author')
        if not self.request.user.groups.filter(name='Author').exists():
            author_group.user_set.add(user)
            form.instance.author_to_user = User.objects.get(pk=self.request.user.id)
            self.object = form.save()
            return redirect('/cabinet')
        else:
            return redirect('/cabinet')


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
    success_url = '/posts/'
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


