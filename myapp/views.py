from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import CanDeletePost, IsNotWeekend  # Import permissions

class PostListCreateView(generics.ListCreateAPIView):
    """View to list all posts or create a new post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsNotWeekend]

    def perform_create(self, serializer):
        """Set the author of the post to the logged-in user."""
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a single post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanDeletePost, IsNotWeekend]

class CommentListCreateView(generics.ListCreateAPIView):
    """View to list all comments for a post or create a new comment."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsNotWeekend]

    def get_queryset(self):
        """Return comments for the specified post."""
        return Comment.objects.filter(post_id=self.kwargs["post_id"])

    def perform_create(self, serializer):
        """Ensure the post exists before creating a comment."""
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a single comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsNotWeekend]
