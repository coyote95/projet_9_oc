"""
This module defines Django models.

Model Classes:
    - Ticket: Represents a ticket with associated information, including user, image, and ticket type.
    - Review: Represents a review associated with a ticket, including rating, user, and comments.
"""


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from PIL import Image


class Ticket(models.Model):
    """
        Represents a ticket with associated information, including user, image, and ticket type.

        Attributes:
            title: CharField
            description: TextField
            user: ForeignKey
            image: ImageField
            uploader: ForeignKey
            time_created: DateTimeField
            ticket_type: CharField ('CREATED', 'REQUEST').
            IMAGE_MAX_SIZE: Tuple (x,y)

        Methods:
            __str__(): Returns a string representation of the ticket, displaying its title.
            resize_image(): Resizes the uploaded image to fit within the specified maximum size.
            save(): Overrides the save method to automatically trigger image resizing on every save.
        """
    TICKET_TYPE_CHOICES = (
        ('CREATED', 'Critique'),
        ('REQUEST', 'Demande'),
    )
    title = models.CharField(max_length=128, verbose_name='titre')
    description = models.TextField(max_length=1000, blank=True, verbose_name="description")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_tickets')
    image = models.ImageField(null=True, blank=True, verbose_name='image')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_tickets')
    time_created = models.DateTimeField(auto_now_add=True)
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)
    IMAGE_MAX_SIZE = (800, 800)

    def __str__(self):
        return f'{self.title}'

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    """
    Represents a review associated with a ticket, including rating, user, and comments.

    Attributes:
        ticket: ForeignKey
        rating: PositiveSmallIntegerField (0 to 5).
        user: ForeignKey
        headline: CharField
        body: TextField
        time_created: DateTimeField

    Methods:
        __str__(): Returns a string representation of the review, indicating the associated ticket and user.
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name='titre')
    body = models.TextField(max_length=1000, blank=True, verbose_name='commentaires')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for Ticket {self.ticket} by {self.user}'
