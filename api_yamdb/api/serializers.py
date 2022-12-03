# from datetime import date as dt
import datetime
from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
