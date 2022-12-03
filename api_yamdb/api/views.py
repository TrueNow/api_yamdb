from .serializers import ReviewSerializer, CommentSerializer
from reviews.models import Comment, Review, User, Title
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from .validators import validate_email, validate_username
from .utils import send_mail

User = get_user_model()


@api_view(['POST'])
def signup_view(request):
    email = request.data.get('email')
    username = request.data.get('username')

    if email is None:
        return Response({'email': 'Email is required.'})

    if not validate_email(email):
        return Response({'email': 'Email is\'n valid.'})

    if username is None:
        return Response({'username': 'Username is required.'})

    if not validate_username(username):
        return Response({'username': f"Incorrect username is '{username}'!"})

    users = User.objects.filter(email=email, username=username)
    if not users.exists():
        User.objects.create(email=email, username=username)

    user = get_object_or_404(User, email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(user.email, confirmation_code)

    return Response(
        {
            'email': email,
            'username': username,
        }
    )


@api_view(['POST'])
def user_token_view(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')

    if username is None:
        return Response({'username': 'Username is required.'})

    if not validate_username(username):
        return Response({'username': f"Incorrect username is '{username}'!"})

    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response('Incorrect pair: username - confirmation_code')
    token = AccessToken.for_user(user)
    return Response({'token': str(token)})


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer


    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
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
