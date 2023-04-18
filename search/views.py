from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from bookstore.models import Book, Author, Category
from bookstore.serializers import BookSerializer, AuthorSerializer, CategorySerializer


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['id', 'title', 'author__name', 'category__name']
    search_fields = ['title', 'author__name', 'category__name']


class AuthorListAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['id', 'name']
    search_fields = ['name']


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['id', 'name']
    search_fields = ['name']
