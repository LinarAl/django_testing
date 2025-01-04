from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from .constants import (DELETE_URL_LITERAL, DETAIL_URL_LITERAL,
                        EDIT_URL_LITERAL, HOME_URL_LITERAL, LOGIN_URL_LITERAL,
                        LOGOUT_URL_LITERAL, SIGNUP_URL_LITERAL)


@pytest.mark.parametrize(
    'name',
    (DETAIL_URL_LITERAL, HOME_URL_LITERAL, LOGIN_URL_LITERAL,
     LOGOUT_URL_LITERAL, SIGNUP_URL_LITERAL)
)
def test_pages_availability_for_anonymous_user(not_author_client, name, news):
    """Страницы detail, home, login, logout, signup доступны анонимному
    пользователю.
    """
    if name != DETAIL_URL_LITERAL:
        url = reverse(name, args=None)
    else:
        url = reverse(name, args=(news.id,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    (EDIT_URL_LITERAL, DELETE_URL_LITERAL),
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, name, comment, expected_status
):
    """Страницы удаления и редактирования комментария доступны автору
    комментария и не доступны другому пользователю.
    """
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (EDIT_URL_LITERAL, DELETE_URL_LITERAL),
)
def test_redirect_for_anonymous_client(client, name, comment):
    """При попытке перейти на страницу редактирования или удаления комментария
    анонимный пользователь перенаправляется на страницу авторизации.
    """
    login_url = reverse(LOGIN_URL_LITERAL)
    url = reverse(name, args=(comment.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
