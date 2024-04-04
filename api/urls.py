from django.urls import path
from api.views import PostAPIView, PostDetailAPIView, AuthorPostAPIView, UserAPIView, UserDetailAPIView


urlpatterns = [
    path('users', UserAPIView.as_view()),
    path('users/<int:id>', UserDetailAPIView.as_view()),
    path('posts', PostAPIView.as_view()),
    path('posts/<int:id>', PostDetailAPIView.as_view()),
    path('authors/<int:id>/posts', AuthorPostAPIView.as_view()),
]