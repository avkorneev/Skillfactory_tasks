from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import os
import sys
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from simpleapp.models import Author, User, Post, Category, Catsubs
from simpleapp.forms import Upgrade, SubscribeForm
from django.contrib.auth.models import Group


sys.path.append(os.path.abspath('..')) #нужно, чтобы избежать ValueError:attempted relative import beyond top-level package


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Author').exists()
        if Author.objects.filter(author_to_user = User(pk=self.request.user.id)):
            context['author'] = Author.objects.get(author_to_user = User(pk=self.request.user.id))
        context['usersubs'] = Category.objects.filter(cat_subscribers = User(pk = self.request.user.id))
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


class Subscribe(LoginRequiredMixin, CreateView):
    template_name = 'subscribe.html'
    form_class = SubscribeForm
    model = Catsubs
    context_object_name = 'subs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usersubs'] = Category.objects.filter(cat_subscribers=User(pk=self.request.user.id)) #юзер выставляется автоматически
        return context


    def form_valid(self,form):
        user = self.request.user
        if not Catsubs.objects.filter(catsubs_to_subs = User.objects.get(pk=user.id)).filter(catsubs_to_cat = form.instance.catsubs_to_cat):  #если этот юзер ещё не подписан на данную категорию
            form.instance.catsubs_to_subs = User.objects.get(pk=user.id)
            self.object = form.save()
        return redirect('/cabinet')


class Unsubscribe(LoginRequiredMixin, DeleteView):
    template_name = 'subscribe.html'
    model = Catsubs
    success_url = '../'

    def get_object(self, queryset = None):   #берём все объекты, принадлежащие данному юзеру
        user = self.request.user
        return Catsubs.objects.filter(catsubs_to_subs=User.objects.get(pk=user.id))  #и удаляем их

