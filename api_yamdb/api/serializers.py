
import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from reviews.models import Review, Title, Comment, User, Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')

    def validate_year(self, value):
        today = datetime.today().year
        if not (today >= value):
            raise serializers.ValidationError('Not valid year!')
        return value


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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
