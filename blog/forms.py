from django import forms
from . import models
from django.shortcuts import get_object_or_404
from authentication.models import User


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget = forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])
        self.fields['rating'].widget.attrs.update({'class': 'radio-inline'})



class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    ticket_type = forms.CharField(widget=forms.HiddenInput(), initial='CREATED')

    class Meta:
        model = models.Ticket
        fields = ['title', 'image', 'description']


class DeleteTicketForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UserFollowsForm(forms.Form):
    username = forms.CharField(label='Nom de l\'utilisateur')



