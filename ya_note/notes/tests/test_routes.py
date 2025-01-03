from http import HTTPStatus

from django.urls import reverse

from .core import TestBase


class TestRoutes(TestBase):

    def test_pages_availability(self):
        """Проверка что анонимный пользователь можнт зайти на страницы: home,
        login, logout, signup.
        """
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):

                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_edit_delete_detail(self):
        """Проверка что только автор заметки может изменить удалить и
        посмотреть заметку.
        """
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.not_author, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:

            self.client.force_login(user)

            for name in ('notes:edit', 'notes:delete', 'notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, kwargs={'slug': self.note.slug})
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_availability_for_notes_add_list_success(self):
        """Проверка что авторизованный пользователь может пройти add, list,
        success.
        """
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.not_author, HTTPStatus.OK),
        )
        for user, status in users_statuses:

            self.client.force_login(user)

            for name in ('notes:add', 'notes:list', 'notes:success'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=None)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Проверка редиректа неавторизованного пользователя."""
        login_url = reverse('users:login')

        for name in (
            'notes:add',
            'notes:list',
            'notes:success',
            'notes:edit',
            'notes:detail',
            'notes:delete',
        ):
            with self.subTest(name=name):
                if name in ('notes:add', 'notes:list', 'notes:success',):
                    url = reverse(name, args=None)
                else:
                    url = reverse(name, kwargs={'slug': self.note.slug})

                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
