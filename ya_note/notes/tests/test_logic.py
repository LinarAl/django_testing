from http import HTTPStatus

from notes.forms import WARNING
from notes.models import Note
from pytils.translit import slugify

from .core import TestBase


class TestNoteCreation(TestBase):
    """Проверка создания заметки."""

    def test_anonymous_user_cant_create_note(self):
        """Проверка создания заметки неавторизованным пользователем."""
        self.client.post(self.ADD_URL, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_user_can_create_note(self):
        """Проверка создания заметки авторизованным пользователем."""
        response = self.auth_client.post(
            self.ADD_URL, data=self.form_data)

        self.assertRedirects(response, self.DONE_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)

        note = Note.objects.get(slug=self.NEW_SLUG)

        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.slug, self.NEW_SLUG)
        self.assertEqual(note.author, self.author)

    def test_not_unique_slug(self):
        """Проверка создания заметки с неуникольным слагом."""
        self.form_data['slug'] = self.USED_SLUG
        response = self.auth_client.post(self.ADD_URL, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=f'{self.USED_SLUG}{WARNING}'
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_empty_slug(self):
        """Если при создании заметки не заполнен slug, то он формируется
        автоматически.
        """
        self.form_data.pop('slug')
        response = self.auth_client.post(
            self.ADD_URL, data=self.form_data)
        self.assertRedirects(response, self.DONE_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)
        new_note = Note.objects.get(id='2')
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_delete_note(self):
        """Проверка удаления заметки ее автором."""
        response = self.auth_client.delete(self.DELETE_URL)
        self.assertRedirects(response, self.DONE_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_note_of_another_user(self):
        """Проверка удаления заметки другим пользователем."""
        response = self.not_author_client.delete(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_note(self):
        """Проверка редактирования заметки ее автором."""
        self.form_data['text'] = self.NEW_NOTE_TEXT
        response = self.auth_client.post(
            self.EDIT_URL, data=self.form_data)
        self.assertRedirects(response, self.DONE_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_comment_of_another_user(self):
        """Проверка редактирования заметки другим пользователем."""
        self.form_data['text'] = self.NEW_NOTE_TEXT
        response = self.not_author_client.post(
            self.EDIT_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)
