from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import User
from bookstore.models import Book

from .serializers import UserSerializer
from bookstore.serializers import BookSerializer


from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .permissions import IsUserOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


import requests
from django.contrib.auth.views import LoginView


class FacebookLoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Please provide a valid access token'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the access token with Facebook
        url = 'https://graph.facebook.com/debug_token'
        params = {'input_token': access_token,
                  'access_token': '35db852826296de1cbf3fe44df6df9c4|54a515d7a0c66b32ea93663015c07e51'}
        response = requests.get(url, params=params).json()

        print('Response : ', response)

        if not response.get('data', {}).get('is_valid'):
            return Response({'error': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the user ID from the access token
        user_id = response['data']['user_id']

        # Get or create the user in your database
        user, created = User.objects.get_or_create(username=user_id)

        # Generate a JWT access token for the user
        refresh = RefreshToken.for_user(user)
        data = {
            'refreshToken': str(refresh),
            'accessToken': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)


class LoginView(APIView, LoginView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        if email is not None:
            user = User.objects.filter(email=email).first()
            day = datetime.now() + timedelta(days=1)

            if user is not None and user.check_password(password):
                token = RefreshToken.for_user(user=user)

                login(request, user=user)
                return Response({
                    'expired': day,
                    'accessToken': str(token.access_token),
                    'refreshToken': str(token)})
            else:
                return Response({'error': 'Invalid email or password.'}, status=404)

        return Response({'error': "Can't be empty email or password."}, status=404)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken(request.data.get('refresh'))
        return Response({
            'accessToken': str(refresh.access_token),
            'refreshToken': str(refresh),
        })


class UserCreateView(generics.CreateAPIView):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsUserOrReadOnly]
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        accessToken = token.split(' ')[1]

        try:
            decoded_token = AccessToken(accessToken)
            decoded_token.verify()
            user = User.objects.get(id=decoded_token['user_id'])

            id = user.id
            email = user.email
            is_verified = user.is_verified
            favorite_books_queryset = user.favorite_books.all()
            favorite_books = BookSerializer(
                favorite_books_queryset, many=True).data
            return Response({'id': id, 'email': str(email), 'isVerified': is_verified, 'favoriteBooks': favorite_books})

        except User.DoesNotExist:
            return Response({'msg': 'user dose not exit.'})
        except Exception as e:
            return Response({'msg': str(e)})


class VerifyEmailView(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('code')

        try:
            user = User.objects.get(email=email, code=verification_code)

            if user.is_verified:
                return Response({'message': 'Your account is verified.'})

            elif user is not None:
                user.is_verified = True
                user.save()
                token = RefreshToken.for_user(user)
                return Response({
                    'accessToken': str(token.access_token),
                    'refreshToken': str(token)})
            else:
                Response({
                    'success': False,
                    'message': 'User Not Found.'
                })

        except User.DoesNotExist:
            return Response({'success': False,
                             'message': 'User Not Found.'})


class FavoriteBookView(generics.GenericAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        user = request.user

        try:
            book = Book.objects.get(id=book_id)
            user.favorite_books.add(book)
            user.save()

        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": True, "user": str(user), "books": str(book)})

    def delete(self, request, book_id):
        user = request.user
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        user.favorite_books.remove(book)
        user.save()

        return Response({'success': True})
