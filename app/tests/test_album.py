from app.models import Album, Photo, User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from . import constants


class AlbumTest(TestCase):
    """Тест API фотоальбома"""
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

    def test_album_not_found(self):
        response = self.client.get('/api/v1/albums/')

        assert response.status_code != 404, (
            'Страница `/api/v1/albums/` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )

    def test_get_not_auth(self):
        response = self.client.get('/api/v1/albums/')

        assert response.status_code == 401, (
            'GET запрос на `/api/v1/albums/` должен быть '
            'доступен только авторизированным пользователям'
        )

    def test_album_get(self):
        response = self.auth_user.get('/api/v1/albums/')

        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/albums/` с токеном '
            'авторизации возвращаетсся статус 200'
        )

        test_data = response.json()

        assert type(test_data) == list, (
            'Проверьте, что при GET запросе на `/api/v1/albums/` '
            'возвращается список'
        )

        assert len(test_data) == Album.objects.filter(
            author=self.user
        ).count(), (
            'Проверьте, что при GET запросе на `/api/v1/albums/` '
            'возвращается список только альбомов пользователя'
        )

        album = Album.objects.get(author=self.user)
        test_album = test_data[0]
        assert 'id' in test_album, (
            'Проверьте, что добавили `id` в список полей `fields` '
            'сериализатора модели Album'
        )
        assert 'name' in test_album, (
            'Проверьте, что добавили `name` в список полей `fields` '
            'сериализатора модели Album'
        )
        assert 'author' in test_album, (
            'Проверьте, что добавили `author` в список полей `fields` '
            'сериализатора модели Album'
        )
        assert 'photo_count' in test_album, (
            'Проверьте, что добавили `photo_count` в список полей `fields` '
            'сериализатора модели Album'
        )
        assert 'created' in test_album, (
            'Проверьте, что добавили `created` в список полей `fields` '
            'сериализатора модели Album'
        )
        assert test_album['author'] == album.author.username, (
            'Проверьте, что `author` сериализатора модели Album возвращает '
            'имя пользователя'
        )

    def test_album_create(self):
        album_count = Album.objects.count()
        data = {}
        response = self.auth_user.post('/api/v1/albums/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/api/v1/albums/` с не '
            'правильными данными возвращается статус 400'
        )
        data = {'name': 'Album_3'}
        response = self.auth_user.post('/api/v1/albums/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/api/v1/albums/` с '
            'правильными данными возвращается статус 201'
        )

        test_data = response.json()
        msg_error = (
            'Проверьте, что при POST запросе на `/api/v1/albums/` возвращается'
            ' словарь с данными нового альбома'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('name') == data['name'], msg_error
        assert test_data.get('author') == self.user.username, (
            'Проверьте, что при POST запросе на `/api/v1/albums/` создается '
            'альбом от авторизованного пользователя'
        )
        assert album_count + 1 == Album.objects.count(), (
            'Проверьте, что при POST запросе на `/api/v1/albums/` создается '
            'альбом'
        )

    def test_album_get_current(self):
        response = self.auth_user.get(f'/api/v1/albums/{self.album_1.id}/')
        assert response.status_code == 200, (
            'Страница `/api/v1/albums/{album_id}/` не найдена, проверьте этот '
            'адрес в *urls.py*'
        )
        photo_count = self.album_1.photo.count()
        test_data = response.json()
        assert test_data.get('name') == self.album_1.name, (
            'Проверьте, что при GET запросе `/api/v1/albums/{album_id}/` '
            'возвращаете значение `name`, должно возвращать название альбома'
        )
        assert test_data.get('author') == self.album_1.author.username, (
            'Проверьте, что при GET запросе `/api/v1/albums/{album_id}/` '
            'возвращаете значение `author`, должно возвращать имя пользователя'
        )
        assert test_data.get('photo_count') == photo_count, (
            'Проверьте, что при GET запросе `/api/v1/albums/{album_id}/` '
            'возвращаете значение `photo_count`, должно возвращать кол-во фото'
        )
        response = self.auth_user.get(f'/api/v1/albums/{self.album_2.id}/')
        assert response.status_code == 404, (
            'Проверьте, что при GET запросе `/api/v1/albums/{album_id}/` для'
            ' не своего альбома возвращаете статус 404'
        )
        Photo.objects.create(
            album=self.album_1,
            name=constants.NAME_PHOTO,
            tag=constants.TAG,
        )
        response = self.auth_user.get(f'/api/v1/albums/{self.album_1.id}/')
        test_data = response.json()
        assert test_data.get('photo_count') == photo_count + 1, (
            'Проверьте, что при GET запросе `/api/v1/albums/{album_id}/` '
            'и изменении кол-во фото в альбоме, возвращаете истинное значение '
            '`photo_count`, должно возвращать кол-во фото'
        )

    def test_album_patch_current(self):
        response = self.auth_user.patch(
            f'/api/v1/albums/{self.album_1.id}/',
            data={'name': 'Поменяли название альбома'}
        )
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/v1/albums/{album_id}/` '
            'возвращаете статус 200'
        )
        test_album = Album.objects.get(id=self.album_1.id)
        assert test_album, (
            'Проверьте, что при PATCH запросе `/api/v1/albums/{album_id}/` '
            'вы не удалили альбом'
        )
        assert test_album.name == 'Поменяли название альбома', (
            'Проверьте, что при PATCH запросе `/api/v1/albums/{album_id}/` '
            'вы изменяете название альбома'
        )
        response = self.auth_user.patch(
            f'/api/v1/albums/{self.album_2.id}/',
            data={'name': 'Поменяли название альбома'}
        )
        assert response.status_code == 404, (
            'Проверьте, что при PATCH запросе `/api/v1/albums/{album_id}/` для'
            ' не своего альбома возвращаете статус 404'
        )

    def test_album_delete(self):
        response = self.auth_user.delete(f'/api/v1/albums/{self.album_1.id}/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/v1/albums/{album_id}/` '
            'возвращаете статус 204'
        )
        test_album = Album.objects.filter(id=self.album_1.id)
        assert not test_album, (
            'Проверьте, что при DELETE запросе `/api/v1/albums/{album_id}/` вы'
            ' удалили альбом'
        )
        response = self.auth_user_2.delete(
            f'/api/v1/albums/{self.album_1.id}/'
        )
        assert response.status_code == 404, (
            'Проверьте, что при DELETE запросе `api/v1/albums/{album_id}/` для'
            ' не своего альбома возвращаете статус 404'
        )
