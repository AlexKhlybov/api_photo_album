import json
from io import BytesIO

from app.models import Album, Photo, User
from django.core.files.base import File
from django.test import TestCase
from PIL import Image
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from . import constants


class PhotoTest(TestCase):
    """Тест API фотографий"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=constants.USERNAME,
            password=constants.PASSWORD
        )
        cls.user_2 = User.objects.create_user(
            username=constants.USERNAME_2,
            password=constants.PASSWORD_2
        )
        cls.client = APIClient()
        token = RefreshToken.for_user(cls.user)
        token_2 = RefreshToken.for_user(cls.user_2)
        cls.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token.access_token}'
        )
        cls.auth_user = cls.client
        cls.client_2 = APIClient()
        cls.client_2.credentials(
            HTTP_AUTHORIZATION=f'Token {token_2.access_token}'
        )
        cls.auth_user_2 = cls.client_2
        cls.album_1 = Album.objects.create(
            name=constants.NAME_1,
            author=cls.user,
        )
        cls.album_2 = Album.objects.create(
            name=constants.NAME_2,
            author=cls.user_2,
        )
        cls.photo_1 = Photo.objects.create(
            album=cls.album_1,
            name=constants.NAME_PHOTO,
            tag=json.dumps(constants.TAG)
        )
        cls.photo_2 = Photo.objects.create(
            album=cls.album_2,
            name=constants.NAME_PHOTO,
            tag=json.dumps(constants.TAG)
        )

    def test_photo_not_found(self):
        response = self.client.get(
            f'/api/v1/albums/{self.album_1.id}/photo/'
        )

        assert response.status_code != 404, (
            'Страница `/api/v1/albums/{album_id}/photo/` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )

    def test_get_not_auth(self):
        response = self.client.get(
            f'/api/v1/albums/{self.album_1.id}/photo/'
        )

        assert response.status_code == 401, (
            'GET запрос на `/api/v1/albums/{album_id}/photo/` должен быть '
            'доступен только авторизированным пользователям'
        )

    def test_photo_get(self):
        response = self.auth_user_2.get(
            f'/api/v1/albums/{self.album_1.id}/photo/'
        )

        assert response.status_code == 403, (
            'Проверьте, что при GET запросе `/api/v1/albums/{album_id}/photo/`'
            ' для чужого альбома возвращаетсся статус 403'
        )

        response = self.auth_user.get(
            f'/api/v1/albums/{self.album_1.id}/photo/'
        )

        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/albums/{album_id}/photo/`'
            ' для своего альбома возвращаетсся статус 200'
        )

        test_data = response.json()
        assert type(test_data) == list, (
            'Проверьте, что при GET запросе на '
            '`/api/v1/albums/{album_id}/photo/` возвращается список'
        )

        assert len(test_data) == Photo.objects.filter(
            album=self.album_1
        ).count(), (
            'Проверьте, что при GET запросе на '
            '`/api/v1/albums/{album_id}/photo/` возвращается список фото, '
            'только этого альбома'
        )

        test_photo = test_data[0]
        assert 'id' in test_photo, (
            'Проверьте, что добавили `id` в список полей `fields` '
            'сериализатора модели Photo'
        )
        assert 'album' in test_photo, (
            'Проверьте, что добавили `album` в список полей `fields` '
            'сериализатора модели Photo'
        )
        assert 'name' in test_photo, (
            'Проверьте, что добавили `name` в список полей `fields` '
            'сериализатора модели Photo'
        )
        assert 'image' in test_photo, (
            'Проверьте, что добавили `image` в список полей `fields` '
            'сериализатора модели Photo'
        )
        assert 'created' in test_photo, (
            'Проверьте, что добавили `created` в список полей `fields` '
            'сериализатора модели Photo'
        )
        assert 'tag' in test_photo, (
            'Проверьте, что добавили `tag` в список полей `fields` '
            'сериализатора модели Photo'
        )
        response = self.client.get(
            f'/api/v1/photos/'
        )
        assert response.status_code == 401, (
            'GET запрос на `/api/v1/photos/` должен быть '
            'доступен только авторизированным пользователям'
        )
        response = self.auth_user.get(
            f'/api/v1/photos/'
        )
        test_data = response.json()
        assert len(test_data) == Photo.objects.filter(
            album__author__username=self.user.username
        ).count(), (
            'Проверьте, что при GET запросе на '
            '`/api/v1/photos/` возвращается список фото, '
            'только этого пользователя'
        )

    def test_photo_create(self):
        photo_count = Photo.objects.filter(album=self.album_1).count()
        data = {}
        response = self.auth_user.post(
            f'/api/v1/albums/{self.album_1.id}/photo/',
            data=data
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на '
            '`/api/v1/albums/{album_id}/photo/` с неправильными данными'
            ' возвращается статус 400'
        )

        file_obj = BytesIO()
        image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
        image.save(file_obj, 'png')
        file_obj.seek(0)
        data = {
            'name': 'Photo_2',
            'album': self.album_1,
            'image': File(file_obj, 'image.png'),
            'tag': json.dumps(constants.TAG),
        }
        response = self.auth_user.post(
            f'/api/v1/albums/{self.album_1.id}/photo/',
            data=data
        )
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на '
            '`/api/v1/albums/{album_id}/photo/` с правильными данными '
            'возвращается статус 201'
        )
        test_data = response.json()
        msg_error = (
            'Проверьте, что при POST запросе на '
            '`/api/v1/albums/{album_id}/photo/` возвращается словарь с '
            'данными нового фото'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('name') == data['name'], msg_error
        photo_add_count = Photo.objects.filter(album=self.album_1).count()
        assert photo_count + 1 == photo_add_count, (
            'Проверьте, что при POST запросе на '
            '`/api/v1/albums/{album_id}/photo/` создается фото'
        )

        file_obj_2 = BytesIO()
        image_2 = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
        image_2.save(file_obj, 'gif')
        file_obj_2.seek(0)
        data = {
            'name': 'Photo_2',
            'album': self.album_1,
            'image': File(file_obj_2, 'image.tif'),
            'tag': json.dumps(constants.TAG),
        }
        response = self.auth_user.post(
            f'/api/v1/albums/{self.album_1.id}/photo/',
            data=data
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на '
            '`/api/v1/albums/{album_id}/photo/` с неправильными данными '
            'возвращается статус 400'
        )

    def test_photo_patch_current(self):
        response = self.auth_user.patch(
            f'/api/v1/albums/{self.album_1.id}/photo/{self.photo_1.id}/',
            data={'name': 'Поменяли название фото'}
        )
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе '
            '`/api/v1/albums/{album_id}/photo/{photo_id}/` '
            'возвращаете статус 200'
        )
        test_photo = Photo.objects.get(id=self.photo_1.id)
        assert test_photo, (
            'Проверьте, что при PATCH запросе '
            '`/api/v1/albums/{album_id}/photo/{photo_id}/` не удалили альбом'
        )
        assert test_photo.name == 'Поменяли название фото', (
            'Проверьте, что при PATCH запросе '
            '`/api/v1/albums/{album_id}/photo/{photo_id}/` '
            'вы изменяете название фото'
        )
        response = self.auth_user.patch(
            f'/api/v1/albums/{self.album_2.id}/photo/{self.photo_2.id}/',
            data={'name': 'Поменяли название альбома'}
        )
        assert response.status_code == 403, (
            'Проверьте, что при PATCH запросе '
            '`/api/v1/albums/{album_id}/photo/{photo_id}/` для не своего '
            'фото возвращаете статус 403'
        )

    def test_photo_delete(self):
        response = self.auth_user.delete(
            f'/api/v1/albums/{self.album_1.id}/photo/{self.photo_1.id}/'
        )
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе '
            '`/api/v1/albums/{album_id}/photo/{photo_id}/` возвращаете '
            'статус 204'
        )
        test_photo = Photo.objects.filter(id=self.photo_1.id)
        assert not test_photo, (
            'Проверьте, что при DELETE запросе '
            '`/api/v1/albums/{album_id}/photo/{photo_id}/` вы удалили альбом'
        )
        response = self.auth_user.delete(
            f'/api/v1/albums/{self.album_2.id}/photo/{self.photo_2.id}/'
        )
        assert response.status_code == 403, (
            'Проверьте, что при DELETE запросе '
            '`api/v1/albums/{album_id}/photo/{photo_id}/` для не своего '
            'фльбома возвращаете статус 403'
        )
