from rest_framework import serializers
from .models import User
from bookstore.serializers import BookSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    favorite_books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'favorite_books', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        favorite_books = data.pop('favorite_books')
        data['favorite_books'] = [book for book in favorite_books]
        return data
