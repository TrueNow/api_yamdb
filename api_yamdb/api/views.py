from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (
    Category, Genre, Title, User, Comment, Review
)

from .permissions import (
    IsUser, IsModerator, IsAdmin, IsAdminUserOrReadOnly, IsAuthor
)
from .serializers import (
    ReviewSerializer, CommentSerializer, TitleSerializer, GenreSerializer,
    CategorySerializer, SignUpSerializer, UserSerializer
)
from .utils import send_mail


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year',)
    permission_classes = (IsAdminUserOrReadOnly,)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        print(filter_kwargs)
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = IsAdminUserOrReadOnly,

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all().aggregate(Avg('score'))

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = IsAdminUserOrReadOnly,

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = IsAdmin,

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class SignUpViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        data = {
            'username': request.data.get('username'),
            'email': request.data.get('email')
        }
        serializer = self.get_serializer(data=data)
        if not self.queryset.filter(**data).exists():
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        user = get_object_or_404(User, **data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(user.email, confirmation_code)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class JWTUserViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if username is None or confirmation_code is None:
            return Response(
                'Incorrect input', status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                'Incorrect pair: username - confirmation_code',
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
