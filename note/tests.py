from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from note.models import Note
from note.forms import NoteCreateForm


class BaseNoteTestCase(TestCase):
    """
    Base class that authenticate the client request.
    """

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


class BaseNoteCreatedTestCases(BaseNoteTestCase):
    """
    Base class that create a new note object.
    """

    def setUp(self):
        super(BaseNoteCreatedTestCases, self).setUp()
        payload = {"title": "new note", "body": "bla bla"}
        self.client.post(reverse('notes:note_create'), payload)
        self.note = Note.objects.get(title=payload["title"])


class NoteAccessDeniedTestCases(TestCase):
    """
    Test each note views to require user to be logged in -- authenticated.
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
    Test create a new note.
    """
    path = reverse('notes:note_create')

    def test_get_note_create(self):
        """
        It loads the page with note form.
        """
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertIn("note/note_form.html", response.template_name)
        self.assertTrue(isinstance(response.context['form'], NoteCreateForm))

    def test_post_note_create_error(self):
        """
        It stays on the same page with form errors.
        """
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], NoteCreateForm))
        self.assertNotEqual(len(response.context['errors']), 0)

    def test_post_note_create_success(self):
        """
        It creates a new note, and redirect to note list.
        """
        payload = {"title": "Another note", "body": "Bla bla bla ..."}
        response = self.client.post(self.path, payload)
        note_exist = Note.objects.filter(title=payload['title']).exists()
        self.assertTrue(note_exist)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, reverse('notes:all'))


class NoteUpdateTestCases(BaseNoteCreatedTestCases):
    """
    Test update a note.
    """

    @property
    def path(self):
        return reverse('notes:note_update', args=(self.note.id,))

    def test_get_note_update_notfound(self):
        """
        It only response for exist note.
        """
        response = self.client.get(reverse('notes:note_update', args=(6,)))
        self.assertEqual(response.status_code, 404)

    def test_get_note_update_found(self):
        """
        It renders note_form with note context variable.
        """
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertIn("note/note_form.html", response.template_name)
        self.assertEqual(response.context['note'], self.note)

    def test_get_note_update_error(self):
        """
        It renders note_form with errors.
        """
        response = self.client.post(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertIn("note/note_form.html", response.template_name)
        self.assertNotEqual(len(response.context['errors']), 0)

    def test_get_note_update_success(self):
        """
        It updates note record and redirect to note detail with the updated info.
        """
        updated_data = {"title": "Updated title", "body": "updated body text"}
        note_detail_path = reverse('notes:note_detail', args=(self.note.id,))
        response = self.client.post(self.path, updated_data)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, note_detail_path)
        updated_response = self.client.get(note_detail_path)
        self.assertEqual(updated_response.status_code, 200)
        self.assertEqual(updated_response.context['note'].title, updated_data['title'])
        self.assertEqual(updated_response.context['note'].body, updated_data['body'])


class NoteDeleteTestCases(BaseNoteCreatedTestCases):
    """
    Test delete a note.
    """

    @property
    def path(self):
        return reverse('notes:note_delete', args=(self.note.id,))

    def test_get_note_delete_view(self):
        """
        It renders the confirm delete template and has the created note object.
        """
        template = 'note/note_confirm_delete.html'
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.note)
        self.assertIn(template, response.template_name)

    def test_post_note_delete_view_success(self):
        """
        It deletes the note and redirect to note list.
        """
        response = self.client.post(self.path)
        is_note = Note.objects.filter(id=self.note.id).exists()
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, reverse('notes:all'))
        self.assertFalse(is_note)


class NoteDetailTestCases(BaseNoteCreatedTestCases):
    """
    Test getting a note detail.
    """

    @property
    def path(self):
        return reverse('notes:note_detail', args=(self.note.id,))

    def test_get_note_detail_view(self):
        """
        It renders the detail template and has the note object.
        """
        template = 'note/note_detail.html'
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.note)
        self.assertIn(template, response.template_name)


class NoteListTestCases(BaseNoteCreatedTestCases):
    """
    Test listing all notes.
    """

    path = reverse('notes:all')

    def test_get_note_list_view(self):
        """
        It renders the note list template and has the note_list object.
        """
        template = 'note/note_list.html'
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)
        self.assertIn(template, response.template_name)
        self.assertIn('note_list', response.context)
        self.assertIn(self.note, response.context['note_list'])

