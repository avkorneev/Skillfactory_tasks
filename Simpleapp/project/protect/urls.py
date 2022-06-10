from django.urls import path
from .views import IndexView, MyPosts, UpgradeAuthor, Subscribe, Unsubscribe

urlpatterns = [
    path('',IndexView.as_view()),
    path('myposts/',MyPosts.as_view()),
    path('upgrade/',UpgradeAuthor.as_view()),
    path('subscribe/', Subscribe.as_view()),
    path('unsubscribe/', Unsubscribe.as_view())
]
