from http import HTTPStatus

import pytest
from django.urls import reverse
from news.forms import WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects

from .constants import (COMMENT_URL_LITERAL, DELETE_URL_LITERAL,
                        DETAIL_URL_LITERAL, EDIT_URL_LITERAL,
                        FORM_COMMENT_BAD_WORDS_DATA, FORM_COMMENT_DATA)


@pytest.mark.parametrize(

    'parametrized_client, comments_count',
    (
        (pytest.lazy_fixture('client'), 0),
        (pytest.lazy_fixture('not_author_client'), 1),
    )
)
@pytest.mark.django_db
def test_parametrized_client_create_comment(
        parametrized_client, comments_count, news):
    """Анонимный пользователь не может отправить комментарий, авторизованный
    пользователь может отправить комментарий.
    """
    url = reverse(DETAIL_URL_LITERAL, args=(news.id,))
    parametrized_client.post(url, data=FORM_COMMENT_DATA)
    assert Comment.objects.count() == comments_count


def test_user_cant_use_bad_words(not_author_client, news):
    """Если комментарий содержит запрещённые слова, он не будет опубликован,
    а форма вернёт ошибку.
    """
    url = reverse(DETAIL_URL_LITERAL, args=(news.id,))
    response = not_author_client.post(url, data=FORM_COMMENT_BAD_WORDS_DATA)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, news, comment):
    """Авторизованный пользователь может редактировать свои комментарии."""
    url = reverse(EDIT_URL_LITERAL, args=(comment.id,))
    news_url = reverse(DETAIL_URL_LITERAL, args=(news.id,))
    url_to_comments = news_url + COMMENT_URL_LITERAL
    response = author_client.post(url, FORM_COMMENT_DATA)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == FORM_COMMENT_DATA['text']


def test_author_can_delete_comment(author_client, news, comment):
    """Авторизованный пользователь может удалять свои комментарии."""
    url = reverse(DELETE_URL_LITERAL, args=(comment.id,))
    news_url = reverse(DETAIL_URL_LITERAL, args=(news.id,))
    url_to_comments = news_url + COMMENT_URL_LITERAL
    response = author_client.post(url, FORM_COMMENT_DATA)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_not_author_can_edit_comment(not_author_client, comment):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    url = reverse(EDIT_URL_LITERAL, args=(comment.id,))
    response = not_author_client.post(url, FORM_COMMENT_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    comment.refresh_from_db()
    assert comment.text == comment_from_db.text


def test_not_author_can_delete_comment(not_author_client, comment):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    url = reverse(DELETE_URL_LITERAL, args=(comment.id,))
    response = not_author_client.post(url, FORM_COMMENT_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
