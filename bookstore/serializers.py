from rest_framework import serializers
from .models import Book, Author, Category


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['authors', 'categories', 'id']

    def get_authors(self, obj):
        return AuthorSerializer(obj.authors.all(), many=True).data

    def get_categories(self, obj):
        return CategorySerializer(obj.categories.all(), many=True).data


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'description', 'coverUrl')


class AuthorDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'description', 'coverUrl', 'books')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )


class CategoryDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'books')
