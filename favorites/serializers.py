from rest_framework import serializers
from .models import FavoriteBook, FavoriteAuthor, FavoriteCategory


class FavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBook
        fields = '__all__'


class FavoriteAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAuthor
        fields = '__all__'


class FavoriteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCategory
        fields = '__all__'
