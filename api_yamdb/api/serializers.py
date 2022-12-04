from rest_framework import serializers

from reviews.models import Review, Title, Comment, User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                'Ранее вы уже оставляли отзыв на данное произведение!')
        return data

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
