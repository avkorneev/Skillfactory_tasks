from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm


class PostAdd(CreateView):
    template_name = 'simpleapp/post_add.html'
    form_class = PostForm


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
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        context['hotpost'] = None
        return context


class PostDetail(DetailView):
    template_name = 'simpleapp/post_details.html'
    queryset = Post.objects.all()


class PostDelete(DeleteView):
    template_name = 'simpleapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


class PostUpdate(UpdateView):
    template_name = 'simpleapp/post_add.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
