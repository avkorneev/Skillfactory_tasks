from django.forms import ModelForm, BooleanField
from .models import Post, Author, User


class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        exclude = ['post_to_postcat','post_rating','post_to_author']


class Upgrade(ModelForm):
    class Meta:
        model = Author
        exclude = ['rating','author_to_user']

