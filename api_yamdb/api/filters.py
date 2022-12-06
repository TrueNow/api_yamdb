from django_filters import rest_framework as drf_filters

from reviews.models import Title


class TitleFilter(drf_filters.FilterSet):
    name = drf_filters.CharFilter(
        field_name='name', lookup_expr='contains'
    )
    category = drf_filters.CharFilter(
        field_name='category__slug', lookup_expr='exact'
    )
    genre = drf_filters.CharFilter(
        field_name='genre__slug', lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year',)
