from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('authors/', views.AuthorListAPIView.as_view(), name='author-list'),
    path('categories/', views.CategoryListAPIView.as_view(), name='category-list'),
]
