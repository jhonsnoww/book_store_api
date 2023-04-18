from rest_framework import serializers
from .models import Book, Author, Category


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField()
    categories = serializers.StringRelatedField()
    author_names = serializers.SerializerMethodField()
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['authors', 'categories', 'id']

    def get_author_names(self, obj):
        try:
            return [author.name for author in obj.authors.all()]
        except:
            return None

    def get_category_names(self, obj):
        try:
            return [category.name for category in obj.categories.all()]
        except:
            return None


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'description', 'photo')


class AuthorDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'description', 'photo', 'books')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class CategoryDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'books')
