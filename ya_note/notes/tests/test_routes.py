from http import HTTPStatus

from django.urls import reverse

from .core import TestBase


class TestRoutes(TestBase):

    def test_pages_availability(self):
        """Проверка что анонимный пользователь может зайти на страницы: home,
        login, logout, signup.
        """
        urls = (
            (self.HOME_URL_LITERAL, None),
            (self.LOGIN_URL_LITERAL, None),
            (self.LOGOUT_URL_LITERAL, None),
            (self.SIGNUP_URL_LITERAL, None),
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

            for name in (self.EDIT_URL_LITERAL, self.DELETE_URL_LITERAL,
                         self.DETAIL_URL_LITERAL):
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

            for name in (self.ADD_URL_LITERAL, self.LIST_URL_LITERAL,
                         self.DONE_URL_LITERAL):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=None)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Проверка редиректа неавторизованного пользователя."""

        for name in (
            self.ADD_URL_LITERAL,
            self.LIST_URL_LITERAL,
            self.DONE_URL_LITERAL,
            self.EDIT_URL_LITERAL,
            self.DETAIL_URL_LITERAL,
            self.DELETE_URL_LITERAL,
        ):
            with self.subTest(name=name):
                if name in (self.ADD_URL_LITERAL, self.LIST_URL_LITERAL,
                            self.DONE_URL_LITERAL,):
                    url = reverse(name, args=None)
                else:
                    url = reverse(name, kwargs={'slug': self.note.slug})

                redirect_url = f'{self.LOGIN_URL}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
