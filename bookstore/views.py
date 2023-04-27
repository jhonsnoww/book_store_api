from .permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status, filters
from .models import Author, Category, Book
from .serializers import AuthorSerializer, CategorySerializer, AuthorDetailSerializer, CategoryDetailSerializer


class BookPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 100


class AuthorList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['name']
    search_fields = ['name']


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        author_serializer = self.get_serializer(instance)
        return Response({
            'authors': author_serializer.data
        })


class CategoryList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['name']
    search_fields = ['^name']


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        category_serializer = self.get_serializer(instance)
        return Response({
            'categories': category_serializer.data
        })


class BookList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['title']
    search_fields = ['^title']

    def list(self, request, *args, **kwargs):

        if request.query_params != None:
            return super().list(request, *args, **kwargs)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        books = serializer.data
        for book in books:
            authors = book.pop('authors')
            categories = book.pop('categories')
            book['authors'] = authors
            book['categories'] = categories
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            book_id = serializer.data.get('id')
            book = Book.objects.get(id=book_id)
            author_ids = request.data.get('authors')
            category_ids = request.data.get('categories')
            authors = Author.objects.filter(id__in=author_ids)
            categories = Category.objects.filter(id__in=category_ids)
            book.authors.set(authors)
            book.categories.set(categories)

            book.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'

    def retrieve(self, request, pk):
        book = self.get_object()
        book.view_count += 1
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookDownloadView(generics.RetrieveAPIView):
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    queryset = Book.objects.all()

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        book.download_count += 1
        book.save()
        return Response({'msg': "success"})
