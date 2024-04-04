from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from api.models import Post, User
from api.serializers import PostSerializer, PostCreateUpdateSerializer, UserSerializer, CreateUserSerializer



class UserAPIView(APIView):
    permission_classes = [IsAdminUser,]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data)


    @swagger_auto_schema(request_body=CreateUserSerializer)
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        data = {
            "data": serializer.data,
            "status": status.HTTP_200_OK,
            "success": True
        }
        return Response(data=data)

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=PostSerializer)
    def post(self, request):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        posts = Post.objects.all()
        for post in posts:
            post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorPostAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        author = get_object_or_404(User, id=id)
        posts = Post.objects.filter(author=author)
        serializer = PostSerializer(posts, many=True)
        data = {
            "data": serializer.data,
            "status": status.HTTP_200_OK,
            "success": True
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        posts = Post.objects.filter(author=author)
        if posts:
            for post in posts:
                post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(post)
        data = {
            "data": serializer.data,
            "status": status.HTTP_200_OK,
            "success": True
        }
        return Response(data=data)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @swagger_auto_schema(request_body=PostCreateUpdateSerializer)
    def patch(self, request, id):
        
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            post = get_object_or_404(Post, id=id)
            post.title = serializer.validated_data.get('title')
            post.content = serializer.validated_data.get('content')
            post.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
