from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserCreateView, LoginView, FacebookLoginView, UserDetailView, FavoriteBookView, CustomTokenRefreshView, VerifyEmailView
urlpatterns = [
    path('auth/refresh', CustomTokenRefreshView.as_view()),
    path('auth/register', UserCreateView.as_view(), name='user-create'),
    path('auth/verify', VerifyEmailView.as_view(), name='user-verify'),
    path('auth/login', LoginView.as_view()),
    path('auth/facebook/login', FacebookLoginView.as_view()),
    path('user/me', UserDetailView.as_view()),
    path('user/favorite/<int:book_id>', FavoriteBookView.as_view())

]
