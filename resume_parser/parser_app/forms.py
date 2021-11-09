from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models



# Create your forms here.
from .models import Customer


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']

        if commit:
            user.save()
            # Creating record in Customer table
            models.Customer.objects.get_or_create(user=user, email=user.email, username=user.username)
        return user

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)