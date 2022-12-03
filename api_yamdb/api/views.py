from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import TitleSerializer
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name', 'year',)

    def perform_create(self, serializer):
        category_slug = self.request.data['category']
        genre_slugs = self.request.data['genre']
        list_genre = []
        category = get_object_or_404(Category, slug=category_slug)
        for genre_slug in genre_slugs:
            list_genre.append(get_object_or_404(Genre, slug=genre_slug))
        serializer.save(category=category, genre=list_genre)

    perform_update = perform_create


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
