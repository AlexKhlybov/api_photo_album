from django.shortcuts import get_object_or_404
from rest_framework import permissions

from app.models import Album


class IsContentAuthor(permissions.BasePermission):
    """Разрешает, если пользователем является автором"""

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
        )


class IsPhotoContentAuthor(permissions.BasePermission):
    """Разрешает, если пользователь является автором альбома"""
    
    def has_permission(self, request, view):
        album = get_object_or_404(Album, id=view.kwargs.get('album_id'))
        return (album.author == request.user)
