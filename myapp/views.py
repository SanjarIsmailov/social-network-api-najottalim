from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import CanDeletePost, IsNotWeekend


# Pagination Classes
class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CommentPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

# Post Views
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related("author").all()  # Optimized Query
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related("author").all()  # Optimized Query
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [CanDeletePost()]
        return [permissions.IsAuthenticatedOrReadOnly]


# Comment Views
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsNotWeekend]
    pagination_class = CommentPagination

    def get_queryset(self):
        return Comment.objects.select_related("author", "post").filter(post_id=self.kwargs["post_id"])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.select_related("author", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsNotWeekend]


# JWT Authentication Views
class JWTLoginView(TokenObtainPairView):
    pass


class JWTLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception:
            return Response({"error": "Invalid token"}, status=400)
