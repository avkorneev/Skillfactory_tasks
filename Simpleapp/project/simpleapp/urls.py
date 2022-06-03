from django.shortcuts import redirect
from django.urls import path

from .views import PostList, PostDetail, PostSearch, PostAdd, PostDelete, PostUpdate, UpgradeAuthor

urlpatterns = [
   path('', PostList.as_view()),
   path('search', PostSearch.as_view()),
   path('add', PostAdd.as_view(), name='post_add'),

   path('<int:pk>', PostDetail.as_view(), name='post_details'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/edit', PostUpdate.as_view(), name='post_add'),
   path('author', UpgradeAuthor.as_view(),name='upgrade')
   ]