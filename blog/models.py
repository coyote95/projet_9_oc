from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from PIL import Image


class Ticket(models.Model):
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
