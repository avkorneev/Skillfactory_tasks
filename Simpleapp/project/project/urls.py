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
    path('posts/', include('simpleapp.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('cabinet/', include('protect.urls')),
    #path('appointments/', include('mails.urls'))
    #path('upgrade/', include('simpleapp.urls'))
    path('task/', include('simpleapp.urls'))

]
