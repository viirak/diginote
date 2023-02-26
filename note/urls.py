from django.urls import path
from note.views import (
    NoteListView,
    NoteDetailView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView)

urlpatterns = [
    path("", NoteListView.as_view(), name="all"),
    path('<int:pk>/detail', NoteDetailView.as_view(), name='note_detail'),
    path('create', NoteCreateView.as_view(), name='note_create'),
    path('<int:pk>/update', NoteUpdateView.as_view(), name='note_update'),
    path('<int:pk>/delete', NoteDeleteView.as_view(), name='note_delete'),
]
