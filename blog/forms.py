"""
This module defines various Django forms.

Form Classes:
    - ReviewForm: Form for creating new reviews.
    - ReviewEditForm: Form for editing existing reviews.
    - DeleteReviewForm: Form for confirming the deletion of a review.
    - TicketForm: Form for creating and editing tickets.
    - DeleteTicketForm: Form for confirming the deletion of a ticket.
    - TicketAndReviewForm: Form combining fields for both tickets and reviews.
    - UserFollowsForm: Form for following users.
"""

from django import forms
from . import models


class ReviewForm(forms.ModelForm):
    """
    Form for creating new reviews.

    Attributes:
        rating: IntegerField
        headline: CharField
        body: CharField
    """

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget = forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])


class ReviewEditForm(forms.ModelForm):
    """
    Form for editing existing reviews.

    Attributes:
        rating: IntegerField
        headline: CharField
        body: CharField
    """

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget = forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])


class DeleteReviewForm(forms.Form):
    """
    Form for confirming the deletion of a review.

    Attributes:
        confirm_delete: BooleanField
    """

    confirm_delete = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))


class TicketForm(forms.ModelForm):
    """
    Form for creating and editing tickets.

    Attributes:
        title: CharField
        image: ImageField
        description: CharField
    """

    ticket_edit = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    ticket_type = forms.CharField(widget=forms.HiddenInput(), initial="CREATED")

    class Meta:
        model = models.Ticket
        fields = ["title", "image", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False


class DeleteTicketForm(forms.Form):
    """
    Form for confirming the deletion of a ticket.

    Attributes:
        confirm_delete: BooleanField
    """

    confirm_delete = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))


class TicketAndReviewForm(forms.ModelForm):
    """
    Form combining fields for both tickets and reviews.

    Attributes:
        title: CharField
        image: ImageField
        description: CharField r
        rating: IntegerField
        body: CharField
    """

    ticket_edit = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    ticket_type = forms.CharField(widget=forms.HiddenInput(), initial="CREATED")

    class Meta:
        model = models.Ticket
        fields = ["title", "image", "description"]

    rating = forms.IntegerField(widget=forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]), label="Rating")
    body = forms.CharField(widget=forms.Textarea(), label="Body")


class UserFollowsForm(forms.Form):
    """
    Form for following users.

    Attributes:
        username: CharField
    """

    username = forms.CharField(label="Nom de l'utilisateur")
