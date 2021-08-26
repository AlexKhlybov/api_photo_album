from app.models import Album, Photo, User
from django.test import TestCase

from . import constants


class AppModelTest(TestCase):
    """Тест моделей"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=constants.USERNAME)
        cls.album = Album.objects.create(
            name=constants.NAME_1,
            author=cls.user,
        )
        cls.photo = Photo.objects.create(
            album=cls.album,
            name=constants.NAME_PHOTO,
            tag=constants.TAG,
        )
        cls.get_verbose_name_album = cls.album._meta.get_field
        cls.get_verbose_name_photo = cls.photo._meta.get_field

    def test_verbose_name_album(self):
        """verbose_name в полях Album совпадает с ожидаемым."""
        field_verboses = {
            'name': 'Название альбома',
            'author': 'Автор',
            'created': 'Дата создания'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_album(value).verbose_name, expected)

    def test_verbose_name_photo(self):
        """verbose_name в полях Photo совпадает с ожидаемым."""
        field_verboses = {
            'album': 'Альбом',
            'name': 'Название',
            'tag': 'Тэг',
            'image': 'Фото',
            'created': 'Дата загрузки'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_photo(value).verbose_name, expected)

    def test_help_text_album(self):
        """help_text в полях Album совпадает с ожидаемым."""
        field_help_texts = {
            'name': 'Название альбома',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_album(value).help_text, expected)

    def test_help_text_photo(self):
        """help_text в полях Photo совпадает с ожидаемым."""
        field_help_texts = {
            'name': 'Название фото',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.get_verbose_name_photo(value).help_text, expected)

    def test_object_name_is_photo(self):
        """__str__  photo - это строчка с содержимым photo.name."""
        photo = AppModelTest.photo
        expected_object_name = photo.name
        self.assertEquals(expected_object_name, str(photo))
