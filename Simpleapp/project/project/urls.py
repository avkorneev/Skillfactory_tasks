from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def redirect_view(request):  # чтобы пустая ссылка перекидывала в посты
    if request:
        response = redirect('/posts/')
    return response


urlpatterns = [
    path('', redirect_view),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
    # подключались к главному приложению с префиксом products/.
    path('posts/', include('simpleapp.urls')),
]
