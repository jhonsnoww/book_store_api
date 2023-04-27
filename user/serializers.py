from rest_framework import serializers
from .models import User
from django.core.mail import send_mail
from django.conf import Settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from bookstore.serializers import BookSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    favorite_books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'is_verified', 'favorite_books', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.create_user(**validated_data)

        verification_code = user.generate_verification_code()
        subject = 'Verify Your Email Address'

        from_email = ""
        context = {'verification_code': verification_code}
        html_message = render_to_string('verification_email.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email,
                  recipient_list=[email], html_message=html_message)

        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        favorite_books = data.pop('favorite_books')
        data['favorite_books'] = [book for book in favorite_books]
        return data
