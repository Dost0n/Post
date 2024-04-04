from rest_framework import serializers
from api.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'password', 'confirm_password')

    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            last_name = validated_data['last_name'],
            first_name = validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    
    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        if password:
            validate_password(password)

        if password != confirm_password:
            raise ValidationError(
                {
                    'message': "Parolingiz va tasdiqlash parolingiz bir biriga teng emas"
                }
            )
        return data
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name","username",)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ("title", "content")

