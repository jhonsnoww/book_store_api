from django.urls import path
from .views import AuthorList, AuthorDetail, CategoryList, CategoryDetail, BookList, BookDetail, BookDownloadView

urlpatterns = [
    path('authors', AuthorList.as_view()),
    path('authors/<int:pk>', AuthorDetail.as_view()),
    path('categories', CategoryList.as_view()),
    path('categories/<int:pk>', CategoryDetail.as_view()),
    path('books', BookList.as_view()),
    path('books/<int:pk>', BookDetail.as_view()),
    path('books/<int:pk>/download',
         BookDownloadView.as_view(), name='book-download'),

]
