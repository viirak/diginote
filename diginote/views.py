from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


class SignupView(View):
    """
    Account signup view.
    """

    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET request; render empty form.
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST request.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('notes:all')
        return render(request, self.template_name, {'form': form})
