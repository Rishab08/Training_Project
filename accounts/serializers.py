from rest_framework import fields, viewsets, serializers, request
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

MIN_LENGTH = 8


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, CustomUser):
        token = super(MyTokenObtainPairSerializer, cls).get_token(CustomUser)

        # Add custom claims
        token['username'] = CustomUser.username
        return token


class SignUpAPISerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=MIN_LENGTH, error_messages={
        "min_length": f"Password must be longer than {MIN_LENGTH} characters."
    }
                                     )
    password2 = serializers.CharField(write_only=True, min_length=MIN_LENGTH,
                                      error_messages={
                                          "min_length": f"Password must be longer than {MIN_LENGTH} characters."
                                          }
                                      )

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password2', 'email', 'date_of_birth', 'phone')

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Password does not match.")

        return data

    def create(self, validated_data):
        all = CustomUser.objects.all()
        username1 = validated_data["username"]
        counter = 1
        for d1 in all:
            if username1 == d1.username:
                username1 = username1 + str(counter)
                counter += 1
                print(username1)
        user = CustomUser.objects.create(
            username=username1,
            email=validated_data["email"],
            phone=validated_data["phone"],
            date_of_birth=validated_data["date_of_birth"],

        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LogInAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'date_of_birth', 'phone')
