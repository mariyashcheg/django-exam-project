from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from .models import Account
from .forms import AccountForm

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'account/account_details.html'

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account  
    form_class = AccountForm
    template_name = 'account/account_edit.html'
    success_url = 'account-details'

    def dispatch(self, request, *args, **kwargs): # new
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        instance = form.save(commit=False)

        if self.request.FILES:
            instance.photo = self.request.FILES.get('photo')

        instance.save()
        return redirect(reverse(self.success_url, kwargs={'pk': instance.pk}))
