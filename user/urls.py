from django.urls import path
from .views import UserCreateView, LoginView, FacebookLoginView, UserDetailView, FavoriteBookView
urlpatterns = [
    path('auth/register', UserCreateView.as_view(), name='user-create'),
    path('auth/login', LoginView.as_view()),
    path('auth/facebook/login', FacebookLoginView.as_view()),
    path('user/me/<int:pk>', UserDetailView.as_view()),
    path('user/favorite/<int:book_id>', FavoriteBookView.as_view())

]
