from django.forms import ModelForm
from note.models import Note

class NoteCreateForm(ModelForm):

    class Meta:
        model = Note
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NoteCreateForm, self).__init__(*args, **kwargs)