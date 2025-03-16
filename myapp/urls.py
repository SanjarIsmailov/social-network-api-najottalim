from django.urls import path
from .views import (
    PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView
)

urlpatterns = [
    # Post endpoints
    path('api/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

    # Comment endpoints
    path('api/posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('api/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
