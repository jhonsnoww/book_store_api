from django.shortcuts import render

from rest_framework import generics, permissions
from .models import (FavoriteBook,
                     FavoriteAuthor,
                     FavoriteCategory)
from .serializers import (FavoriteBookSerializer,
                          FavoriteAuthorSerializer,
                          FavoriteCategorySerializer)


class FavoriteBookList(generics.ListCreateAPIView):
    queryset = FavoriteBook.objects.all()
    serializer_class = FavoriteBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteAuthorList(generics.ListCreateAPIView):
    queryset = FavoriteAuthor.objects.all()
    serializer_class = FavoriteAuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteCategoryList(generics.ListCreateAPIView):
    queryset = FavoriteCategory.objects.all()
    serializer_class = FavoriteCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
