from http import HTTPStatus

import pytest
from django.urls import reverse
from news.forms import WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.parametrize(

    'parametrized_client, comments_count',
    (

        (pytest.lazy_fixture('client'), 0),
        (pytest.lazy_fixture('not_author_client'), 1),
    )
)
@pytest.mark.django_db
def test_parametrized_client_create_comment(
        parametrized_client, comments_count, news, form_comment_data):
    """Анонимный пользователь не может отправить комментарий, авторизованный
    пользователь может отправить комментарий."""
    url = reverse('news:detail', args=(news.id,))
    parametrized_client.post(url, data=form_comment_data)
    assert Comment.objects.count() == comments_count


def test_user_cant_use_bad_words(
        not_author_client, news, form_comment_bad_words_data
):
    """Если комментарий содержит запрещённые слова, он не будет опубликован,
    а форма вернёт ошибку."""
    url = reverse('news:detail', args=(news.id,))
    response = not_author_client.post(url, data=form_comment_bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
        author_client, news, comment, form_comment_data
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    url = reverse('news:edit', args=(comment.id,))
    news_url = reverse('news:detail', args=(news.id,))
    url_to_comments = news_url + '#comments'
    response = author_client.post(url, form_comment_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_comment_data['text']


def test_author_can_delete_comment(
        author_client, news, comment, form_comment_data
):
    """Авторизованный пользователь может удалять свои комментарии."""
    url = reverse('news:delete', args=(comment.id,))
    news_url = reverse('news:detail', args=(news.id,))
    url_to_comments = news_url + '#comments'
    response = author_client.post(url, form_comment_data)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_not_author_can_edit_comment(
        not_author_client, comment, form_comment_data
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, form_comment_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    comment.refresh_from_db()
    assert comment.text == comment_from_db.text


def test_not_author_can_delete_comment(
        not_author_client, comment, form_comment_data
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    url = reverse('news:delete', args=(comment.id,))
    response = not_author_client.post(url, form_comment_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
