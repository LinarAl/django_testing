from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestBase(TestCase):

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
        cls.LOGIN_URL = reverse('users:login')
        cls.LIST_URL = reverse('notes:list')
        cls.ADD_URL = reverse('notes:add', args=None)
        cls.EDIT_URL = reverse('notes:edit', kwargs={'slug': cls.note.slug})
        cls.DELETE_URL = reverse('notes:delete', kwargs={
                                 'slug': cls.note.slug})
        cls.DONE_URL = reverse('notes:success', args=None)

        cls.form_data = {'title': cls.NOTE_TITLE,
                         'text': cls.NOTE_TEXT, 'slug': cls.NEW_SLUG}
