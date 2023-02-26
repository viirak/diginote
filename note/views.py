from django.shortcuts import redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from note.models import Note
from note.forms import NoteCreateForm



class NoteBaseView(View):
    """
    Base view for create, list, detail, update and delete class views.
    """
    model = Note

    # protect inheritor views from anonyous
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SingleNoteBaseView(NoteBaseView):
    """
    Base view for detail, update, and delete class views.
    """

    def get_queryset(self):
        """
        Override the default queryset
        to protect access beside the owner.
        """
        return Note.objects.filter(id=self.kwargs["pk"], user=self.request.user)


class NoteCreateView(NoteBaseView, CreateView):
    """
    Generic detail view
    template name: note/note_form.html
    """
    form_class = NoteCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect("notes:all")

    def get_form_kwargs(self, *args, **kwargs):
        """
        Override the submitted form values to add the "user" value
        """
        kwargs = super(NoteCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class NoteListView(NoteBaseView, ListView):
    """
    Generic detail view
    template name: note/note_list.html
    context variables include 'note_list' object name
    """

    def get_queryset(self):
        """
        Override the default queryset to only get notes owned by the user.
        """
        qs = Note.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', "")
        return context


class NoteDetailView(SingleNoteBaseView, DetailView):
    """
    Generic detail view
    template name: note/note_detail.html
    context variables include 'note' object name
    query_set is defined in SingleNoteBaseView
    """

class NoteUpdateView(SingleNoteBaseView, UpdateView):
    """
    Generic update view
    template name: note/note_form.html
    context variables include 'note' object name
    """
    fields = ['title', 'body'] # fields to be updated

    def get_success_url(self, **kwargs):
        """
        Url to be redirected to when update successful.
        """
        return reverse_lazy("notes:note_detail", args=(self.kwargs["pk"],))


class NoteDeleteView(SingleNoteBaseView, DeleteView):
    """
    Generic delete view
    template: note/note_confirm_delete.html
    context variables include 'note' object name
    """
    success_url = reverse_lazy("notes:all") # redirect to on success
