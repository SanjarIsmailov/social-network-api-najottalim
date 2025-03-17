from django.utils import timezone
from rest_framework import permissions
from datetime import timedelta
from .models import Comment

class CanDeletePost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE" and request.user == obj.author:
            current_time = timezone.localtime(timezone.now())
            post_age = current_time - obj.created_at
            has_comments = Comment.objects.filter(post=obj).exists()
            return post_age < timedelta(minutes=2) or not has_comments
        return False

class IsNotWeekend(permissions.BasePermission):
    def has_permission(self, request, view):
        return timezone.localtime(timezone.now()).weekday() not in [1, 2]
