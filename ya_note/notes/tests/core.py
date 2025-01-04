from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestBase(TestCase):
    """Базовый класс и фикстурами"""

    @classmethod
    def setUpTestData(cls):

        cls.NOTE_TITLE = 'title'
        cls.NOTE_TEXT = 'text'
        cls.NEW_NOTE_TEXT = 'new text'
        cls.USED_SLUG = 'slug'
        cls.NEW_SLUG = 'slug2'

        cls.author = User.objects.create(username='Лев Толстой')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)

        cls.not_author = User.objects.create(username='Читатель простой')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

        cls.note = Note.objects.create(
            title='Заголовок',
            text=cls.NOTE_TEXT,
            slug=cls.USED_SLUG,
            author=cls.author
        )
        cls.LOGIN_URL_LITERAL = 'users:login'
        cls.LOGOUT_URL_LITERAL = 'users:logout'
        cls.SIGNUP_URL_LITERAL = 'users:signup'

        cls.HOME_URL_LITERAL = 'notes:home'
        cls.LIST_URL_LITERAL = 'notes:list'
        cls.ADD_URL_LITERAL = 'notes:add'
        cls.EDIT_URL_LITERAL = 'notes:edit'
        cls.DELETE_URL_LITERAL = 'notes:delete'
        cls.DETAIL_URL_LITERAL = 'notes:detail'
        cls.DONE_URL_LITERAL = 'notes:success'

        cls.LOGIN_URL = reverse(cls.LOGIN_URL_LITERAL)
        cls.LOGOUT_URL = reverse(cls.LOGOUT_URL_LITERAL)
        cls.SIGNUP_URL = reverse(cls.SIGNUP_URL_LITERAL)

        cls.HOME_URL = reverse(cls.HOME_URL_LITERAL)
        cls.LIST_URL = reverse(cls.LIST_URL_LITERAL)
        cls.ADD_URL = reverse(cls.ADD_URL_LITERAL, args=None)
        cls.EDIT_URL = reverse(cls.EDIT_URL_LITERAL, kwargs={
                               'slug': cls.note.slug})
        cls.DELETE_URL = reverse(cls.DELETE_URL_LITERAL, kwargs={
                                 'slug': cls.note.slug})
        cls.DONE_URL = reverse(cls.DONE_URL_LITERAL, args=None)

        cls.form_data = {'title': cls.NOTE_TITLE,
                         'text': cls.NOTE_TEXT, 'slug': cls.NEW_SLUG}
