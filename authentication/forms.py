"""
This module provides a custom form, SignupForm, based on Django's UserCreationForm,
for user registration with additional fields such as first name, last name, and email.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name")
