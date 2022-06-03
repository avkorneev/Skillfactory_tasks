from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import os
import sys
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from simpleapp.models import Author, User, Post
from simpleapp.forms import Upgrade
from django.contrib.auth.models import Group

sys.path.append(os.path.abspath('..')) #нужно, чтобы избежать ValueError:attempted relative import beyond top-level package


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Author').exists()
        if Author.objects.filter(author_to_user = User(pk=self.request.user.id)):
            context['author'] = Author.objects.get(author_to_user = User(pk=self.request.user.id))
        return context


class MyPosts(LoginRequiredMixin, ListView):
    template_name = 'myposts.html'
    model = Post
    ordering = '-post_datetime'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Post.objects.filter(post_to_author=Author.objects.get(author_to_user=User(pk=self.request.user.id)))
        context['filter'] = queryset
        return context


class UpgradeAuthor(LoginRequiredMixin, CreateView):
    template_name = 'sign/upgrade.html'
    form_class = Upgrade
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Author').exists()
        if Author.objects.filter(author_to_user = User(pk=self.request.user.id)):
            context['author'] = Author.objects.get(author_to_user = User(pk=self.request.user.id))
        return context

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

