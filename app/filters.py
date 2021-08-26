import django_filters

from .models import Photo


class PhotoFilter(django_filters.FilterSet):
    """Фильтр фото по альбому и тегам"""
    album = django_filters.CharFilter(
        field_name='album__name',
        lookup_expr='icontains'
    )
    tag = django_filters.CharFilter(
        field_name='tag__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Photo
        fields = ('album', 'tag')
