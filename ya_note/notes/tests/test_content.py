from notes.forms import NoteForm

from .core import TestBase


class TestListPage(TestBase):
    """Проверка страницы со списком заметок."""

    def test_notes_list_for_author(self):
        """Отдельная заметка передаётся на страницу со списком заметок."""
        response = self.auth_client.get(self.LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_notes_list_for_reader(self):
        """В список заметок одного пользователя не попадают заметки другого."""
        response = self.not_author_client.get(self.LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)


class TestAddDetailDeletePages(TestBase):
    """Проверка наличии и отсутсвия формы на страницах add, edit."""

    def test_authorized_client_add_has_form(self):
        """Проверка наличия формы на страницы add."""
        response = self.auth_client.get(self.ADD_URL)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_authorized_client_edit_has_form(self):
        """Проверка наличия формы на страницы edit."""
        response = self.auth_client.get(self.EDIT_URL)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
