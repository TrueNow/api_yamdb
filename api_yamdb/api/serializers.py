from django.contrib.auth import get_user_model
from reviews.models import Review
from rest_framework import serializers

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'scope', 'pub_date')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username', 'role')
        model = User
