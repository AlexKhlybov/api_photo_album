from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('v1/albums', views.AlbumViewSet, basename='AlbumView')
router_v1.register(
    r'v1/albums/(?P<album_id>\d+)/photo',
    views.PhotoAlbumViewSet,
    basename='PhotoAlbumView'
)
router_v1.register('v1/photos', views.PhotoViewSet, basename='PhotoView')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
