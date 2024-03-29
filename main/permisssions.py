from rest_framework.permissions import BasePermission


class ApplicationPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_master)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user.is_master or request.user.is_staff)

class IsApplicationAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author_id == request.user

class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user