import os
from django.conf import settings
from .permissions import IsAdminOrReadOnly


from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status
from .models import Author, Category, Book
from .serializers import AuthorSerializer, CategorySerializer, AuthorDetailSerializer, CategoryDetailSerializer
from rest_framework.parsers import FileUploadParser, MultiPartParser


class BookPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 100


class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        photo = self.request.data.get('photo')
        if photo:
            filename = os.path.join('photos', photo.name)
            filepath = 'media/{}'.format(photo.name)
            with open(filepath, 'wb') as f:
                for chunk in photo.chunks():
                    f.write(chunk)
            serializer.validated_data['photo'] = filename

        # Save the author object
        serializer.save()

    def perform_update(self, serializer):
        # Get the uploaded photo from the request
        photo = self.request.data.get('photo')
        if photo:
            # Construct the path to save the file
            filename = os.path.join('photos', photo.name)
            filepath = os.path.join(settings.BASE_DIR, filename)

            # Save the file to the desired path
            with open(filepath, 'wb') as f:
                for chunk in photo.chunks():
                    f.write(chunk)

            # Update the photo field in the serializer with the saved path
            serializer.validated_data['photo'] = filename

        # Save the author object
        serializer.save()


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        author_serializer = self.get_serializer(instance)
        return Response({
            'author': author_serializer.data
        })


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # apply the custom permission here
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    # apply the custom permission here
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        category_serializer = self.get_serializer(instance)
        return Response({
            'category': category_serializer.data
        })


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    permission_classes = [IsAdminOrReadOnly] # apply the custom permission here


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        books = serializer.data
        for book in books:
            authors = book.pop('author_names')
            categories = book.pop('category_names')
            book['authors'] = authors
            book['categories'] = categories
        return Response(books)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            book_id = serializer.data.get('id')
            book = Book.objects.get(id=book_id)
            author_ids = request.data.getlist('authors')
            category_ids = request.data.getlist('categories')
            authors = Author.objects.filter(id__in=author_ids)
            categories = Category.objects.filter(id__in=category_ids)

            file = request.data.get('pdf')

            filepath = f'pdfs/{book.title}.pdf'

            with open(filepath, 'wb') as f:
                f.write(file.read())

            book.pdf = filepath
            book.authors.set(authors)
            book.categories.set(categories)

            book.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
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
        # delete the associated pdf file
        if instance.pdf and os.path.exists(instance.pdf.path):
            os.remove(instance.pdf.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookDownloadView(generics.RetrieveAPIView):
    queryset = Book.objects.all()

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        book.download_count += 1
        book.save()
        return Response({'msg': "success"})
