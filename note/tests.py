from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from note.models import Note
from note.forms import NoteCreateForm


class BaseNoteTestCase(TestCase):

    username = "tempusername"
    password = "temppassword"

    def create_test_user(self):
        User = get_user_model()
        user = User.objects.create_user(username=self.username)
        user.set_password(self.password)
        user.save()

    def authenticate_test_user(self):
        self.client.login(username=self.username, password=self.password)

    def setUp(self):
        self.create_test_user()
        self.authenticate_test_user()


class NoteAccessDeniedTestCases(TestCase):
    """
    Test login requried for each note views.
    """

    def test_list_view(self):
        response = self.client.get(reverse('notes:all'))
        self.assertEqual(response.status_code, 302)

    def test_create_view(self):
        response = self.client.get(reverse('notes:note_create'))
        self.assertEqual(response.status_code, 302)

    def test_detail_view(self):
        response = self.client.get(reverse('notes:note_detail', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_update_view(self):
        response = self.client.get(reverse('notes:note_update', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_delete_view(self):
        response = self.client.get(reverse('notes:note_delete', args=(1,)))
        self.assertEqual(response.status_code, 302)


class NoteCreateTestCases(BaseNoteTestCase):
    """
    """
    path = reverse('notes:note_create')

    def test_get_note_create(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], NoteCreateForm))

    def test_post_note_create_error(self):
        response = self.client.post(self.path)
        self.assertFalse(isinstance(response, HttpResponseRedirect))
        self.assertTrue(isinstance(response.context['form'], NoteCreateForm))
        self.assertNotEqual(len(response.context['errors']), 0)

    def test_post_note_create_success(self):
        payload = {"title": "New note 1", "body": "Bla bla bal"}
        response = self.client.post(self.path, payload)
        note_exist = Note.objects.filter(title=payload['title']).exists()
        self.assertTrue(note_exist)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, reverse('notes:all'))


class NoteUpdateTestCases(BaseNoteTestCase):
    """
    """

    def setUp(self):
        super(NoteUpdateTestCases, self).setUp()
        payload = {"title": "new note", "body": "bla bla"}
        self.client.post(reverse('notes:note_create'), payload)
        self.note = Note.objects.get(title=payload["title"])

    def get_note_path(self, id):
        return reverse('notes:note_update', args=(id,))

    def test_get_note_update_notfound(self):
        response = self.client.get(self.get_note_path(5))
        self.assertEqual(response.status_code, 404)

    def test_get_note_update_found(self):
        response = self.client.get(self.get_note_path(self.note.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['note'], self.note)

    def test_get_note_update_error(self):
        response = self.client.post(self.get_note_path(self.note.id), {})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.context['errors']), 0)

    def test_get_note_update_success(self):
        updated_data = {"title": "Updated title", "body": "updated body text"}
        note_detail_path = reverse('notes:note_detail', args=(self.note.id,))
        response = self.client.post(self.get_note_path(self.note.id), updated_data)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, note_detail_path)
        updated_response = self.client.get(note_detail_path)
        self.assertEqual(updated_response.status_code, 200)
        self.assertEqual(updated_response.context['note'].title, updated_data['title'])
        self.assertEqual(updated_response.context['note'].body, updated_data['body'])
