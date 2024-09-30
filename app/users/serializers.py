from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    def save(self, **kwargs):
        email = self.validated_data.get("email")
        username = self.validated_data.get("username")
        password = self.validated_data.get("password")
        first_name = self.validated_data.get("first_name", "")
        last_name = self.validated_data.get("last_name", "")

        if User.objects.filter(email=email).exists():
            raise ValidationError({"email": ["Email already exists."]})

        if User.objects.filter(username=username).exists():
            raise ValidationError({"username": ["Username already exists."]})

        return User.objects.create_user(
            username, email, password, first_name=first_name, last_name=last_name
        )
