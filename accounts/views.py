from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('tasks:message', kwargs={'type': 'signup'})
    template_name = 'registration/signup.html'


@login_required
def user_page(request):
    return render(request, 'accounts/user_page.html')
