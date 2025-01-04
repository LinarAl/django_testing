import pytest
from django.conf import settings
from django.urls import reverse

from .constants import DETAIL_URL_LITERAL, HOME_URL_LITERAL


@pytest.mark.django_db
def test_news_count(client, news_list):
    """Количество новостей на главной странице — не более 10."""
    url = reverse(HOME_URL_LITERAL)
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_list):
    """Новости отсортированы от самой свежей к самой старой."""
    url = reverse(HOME_URL_LITERAL)
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news, comments_list):
    """Комментарии на странице отдельной новости отсортированы в
    хронологическом порядке: старые в начале списка, новые — в конце.
    """
    url = reverse(DETAIL_URL_LITERAL, args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    'parametrized_client, form_in_context',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('not_author_client'), True),
    )
)
@pytest.mark.django_db
def test_parametrized_client_has_or_no_form(
    news, parametrized_client, form_in_context
):
    """Анонимному пользователю недоступна форма для отправки комментария на
    странице отдельной новости, а авторизованному доступна.
    """
    url = reverse(DETAIL_URL_LITERAL, args=(news.id,))
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_in_context
