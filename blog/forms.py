from django import forms
from . import models


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'image', 'caption', 'description']


class DeleteTicketForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
