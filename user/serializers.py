from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    favorite_books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'favorite_books', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_favorite_books(self, obj):
        try:
            return [favbook for favbook in obj.favorite_books.all()]
        except:
            return None
