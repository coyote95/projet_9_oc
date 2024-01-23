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


class ReviewEditForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget = forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])


class DeleteReviewForm(forms.Form):
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class TicketForm(forms.ModelForm):
    ticket_edit = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    ticket_type = forms.CharField(widget=forms.HiddenInput(), initial='CREATED')

    class Meta:
        model = models.Ticket
        fields = ['title', 'image', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


class DeleteTicketForm(forms.Form):
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class TicketAndReviewForm(forms.ModelForm):
    ticket_edit = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    ticket_type = forms.CharField(widget=forms.HiddenInput(), initial='CREATED')

    class Meta:
        model = models.Ticket
        fields = ['title', 'image', 'description']

    # Champs spécifiques à la review
    rating = forms.IntegerField(
        widget=forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        label='Rating'
    )
    body = forms.CharField(widget=forms.Textarea(), label='Body')


class UserFollowsForm(forms.Form):
    username = forms.CharField(label='Nom de l\'utilisateur')
