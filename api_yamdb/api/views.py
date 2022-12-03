from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken
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
