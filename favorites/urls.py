from django.urls import path
from .views import (FavoriteBookList,
                    FavoriteAuthorList,
                    FavoriteCategoryList)

urlpatterns = [
    path('books/favorites', FavoriteBookList.as_view()),
    path('authors/favorites', FavoriteAuthorList.as_view()),
    path('categories/favorites', FavoriteCategoryList.as_view()),

]
