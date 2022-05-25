from django_filters import FilterSet, DateFilter, CharFilter
from django.forms import DateInput
from .models import Post


class PostFilter(FilterSet):
    rating = CharFilter(field_name='post_rating', lookup_expr='gt', label='Posts with rating greater than')
    author = CharFilter(field_name='post_to_author__name', lookup_expr='icontains', label='Author name contains')
    start_datetime = DateFilter(field_name='post_datetime', widget=DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'value': "2021/01/01"}), lookup_expr='gt', label='Posts since')
    end_datetime = DateFilter(field_name='post_datetime', widget=DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'value': "2021/01/01"}), lookup_expr='lt', label='Post until')

    # Оно работает, и это чудо (я про виджеты даты)
    class Meta:
        model = Post
        fields = {

        }
