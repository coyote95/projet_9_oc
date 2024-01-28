"""
This module provides views for user authentication, including user logout and signup.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.conf import settings
from . import forms


def logout_user(request):
    logout(request)
    return redirect("login")


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", context={"form": form})
