from django import forms
from . import models


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    ticket_type = forms.CharField(widget=forms.HiddenInput(), initial='CREATED')

    class Meta:
        model = models.Ticket
        fields = ['title', 'image', 'description']


class DeleteTicketForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
