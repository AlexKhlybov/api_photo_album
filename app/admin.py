from django.contrib import admin

from .models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """Админка альбомов"""
    list_display = ('pk', 'name', 'author', 'photo_count', 'created')
    search_fields = ('name',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Photo)
class ImageAdmin(admin.ModelAdmin):
    """Админка фотографий"""
    list_display = (
        'pk',
        'album',
        'name',
        'tag',
        'image',
        'image_thumbnail',
        'created'
    )
    search_fields = ('name',)
    list_filter = ('album',)
    empty_value_display = '-пусто-'
