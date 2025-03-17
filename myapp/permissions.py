from datetime import timedelta

from django.utils import timezone
from rest_framework import permissions


class CanDeletePost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE" and request.user == obj.author:
            current_time = timezone.localtime(timezone.now())
            post_age = current_time - obj.created_at
            return post_age < timedelta(minutes=2)
        return False

class IsNotWeekend(permissions.BasePermission):
    def has_permission(self, request, view):
        return timezone.localtime(timezone.now()).weekday() not in [5, 6]
