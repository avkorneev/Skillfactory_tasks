from django.urls import path
from .views import IndexView, MyPosts, UpgradeAuthor

urlpatterns = [
    path('',IndexView.as_view()),
    path('myposts/',MyPosts.as_view()),
    path('upgrade/',UpgradeAuthor.as_view())
]
