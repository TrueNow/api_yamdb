import datetime
from rest_framework import serializers
from reviews.models import Review, Title, Comment, User, Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'category', 'genre', 'name', 'year')

    def validate_year(self, value):
        today = datetime.datetime.today().year
        if today < value:
            raise serializers.ValidationError('Not valid year!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    # def validate(self, data):
    #     if self.context['request'].method == 'PATCH':
    #         return data
    #     title = self.context['view'].kwargs['title_id']
    #     author = self.context['request'].user
    #     if Review.objects.filter(author=author, title__id=title).exists():
    #         raise serializers.ValidationError(
    #             'Ранее вы уже оставляли отзыв на данное произведение!')
    #     return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_role(self, value):
        user = self.context.get('request').user
        if not (user.is_admin or user.is_moderator):
            return 'user'
        return value


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        error_names = ('me',)
        username = value
        if username in error_names:
            raise serializers.ValidationError(
                f'Нельзя использовать имя {username}'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
