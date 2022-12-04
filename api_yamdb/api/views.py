from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title, User, Comment, Review

from .serializers import (
    ReviewSerializer, CommentSerializer, TitleSerializer, GenreSerializer,
    CategorySerializer, SignUpSerializer, UserSerializer, JWTUserSerializer
)
from .utils import send_mail


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
    serializer_class = GenreSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    serializer_class = CategorySerializer

class SignUpViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        if not self.queryset.filter(**serializer.validated_data).exists():
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        username = request.data.get('username')
        email = request.data.get('email')
        user = self.queryset.get(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(user.email, confirmation_code)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class JWTUserViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = JWTUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        username = serializer.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response('Incorrect pair: username - confirmation_code',
                            status=status.HTTP_400_BAD_REQUEST)
        token = AccessToken.for_user(user)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id),
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id),
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)
