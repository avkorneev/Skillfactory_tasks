from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from .models import Post, Author, User, Postcat, Category, Catsubs


class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        exclude = ['post_rating', 'post_to_author']

    post_to_postcat = ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple
    )


class Upgrade(ModelForm):
    class Meta:
        model = Author
        exclude = ['rating', 'author_to_user']


class SubscribeForm(ModelForm):
    class Meta:
        model = Catsubs
        fields = ['catsubs_to_cat']
        labels = {
            'catsubs_to_cat':'Выберите категорию:'
        }

    #как сделать несколько галочек сразу - пока не знаю. Вылезает QuerySet, а переписать post под него пока не вышло
    #catsubs_to_cat = ModelMultipleChoiceField(
    #    queryset=Category.objects.all(),
    #    widget=CheckboxSelectMultiple
    #)


