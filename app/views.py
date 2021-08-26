from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.filters import PhotoFilter

from .models import Album, Photo
from .permissions import IsContentAuthor, IsPhotoContentAuthor
from .serializers import AlbumSerializer, PhotoAlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    """Представление альбомов"""

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated, IsContentAuthor]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created', 'photo_count']

    def get_queryset(self):
        return self.queryset.filter(
            author=self.request.user
        ).annotate(photo_count=Count('photo'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PhotoAlbumViewSet(viewsets.ModelViewSet):
    """Представления фотографий в альбоме"""

    queryset = Photo.objects.all()
    serializer_class = PhotoAlbumSerializer
    permission_classes = [IsAuthenticated, IsPhotoContentAuthor]

    def list(self, request, album_id):
        data = self.queryset.filter(album_id=album_id)
        return Response(self.serializer_class(data, many=True).data)

    def perform_create(self, serializer):
        album = get_object_or_404(Album, id=self.kwargs.get('album_id'))
        serializer.save(album_id=album.id)


class PhotoViewSet(viewsets.ModelViewSet):
    """Представление всех фотографий пользователя"""

    queryset = Photo.objects.all()
    serializer_class = PhotoAlbumSerializer
    permission_classes = [IsAuthenticated, ]
    filterset_class = PhotoFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['album', 'created']

    def get_queryset(self):
        return self.queryset.filter(album__author=self.request.user)
