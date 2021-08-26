# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
# imagekit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
# taggit
from taggit.managers import TaggableManager

User = get_user_model()


class Album(models.Model):
    """Альбом с фотографиями"""
    name = models.CharField(
        'Название альбома',
        max_length=200,
        help_text='Название альбома'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='albums'
    )
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self) -> str:
        return self.name

    def photo_count(self) -> int:
        """Считает кол-во фото в альбоме """
        return self.photo.count()

    class Meta:
        ordering = ('created',)
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Photo(models.Model):
    """Фотография в альбоме"""
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='photo',
        verbose_name='Альбом'
    )
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Название фото'
    )
    tag = TaggableManager(
        verbose_name='Тэг',
        related_name='tags',
        blank=False
    )
    image = models.ImageField(
        upload_to='app/',
        blank=False,
        null=False,
        verbose_name='Фото',
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFit(width=settings.WIDTH, upscale=False)],
        format='JPEG',
        options={'quality': settings.QUALITY},
    )
    created = models.DateTimeField(
        'Дата загрузки',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('created',)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
