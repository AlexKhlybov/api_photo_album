from rest_framework import serializers
from taggit_serializer.serializers import (TaggitSerializer,
                                           TagListSerializerField)

from .ImageChecker import check_image
from .models import Album, Photo


class AlbumSerializer(serializers.ModelSerializer):
    """Сериализатор альбома"""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'author',
            'photo_count',
            'created'
        )
        model = Album
        read_only_fields = ('created', )


class PhotoAlbumSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Сериализатор фотографий в альбоме"""
    
    album = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    tag = TagListSerializerField()
    image = serializers.ImageField(validators=[check_image])
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        fields = (
            'id',
            'album',
            'name',
            'image',
            'image_thumbnail',
            'created',
            'tag'
        )
        read_only_fields = ('created', 'image')
        model = Photo
