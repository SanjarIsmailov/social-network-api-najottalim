from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView, JWTLoginView, JWTLogoutView
)

urlpatterns = [
    # Post endpoints
    path("api/posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("api/posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),

    # Comment endpoints
    path("api/posts/<int:post_id>/comments/", CommentListCreateView.as_view(), name="comment-list-create"),
    path("api/comments/<int:pk>/", CommentDetailView.as_view(), name="comment-detail"),

    path('login/', JWTLoginView.as_view(), name='jwt-login'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('logout/', JWTLogoutView.as_view(), name='jwt-logout'),
]
