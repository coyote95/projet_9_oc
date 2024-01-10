from django.db import models
from django.conf import settings
from PIL import Image


class Ticket(models.Model):
    TICKET_TYPE_CHOICES = (
        ('CREATED', 'Critique'),
        ('REQUEST', 'Demande'),
    )
    title = models.CharField(max_length=128, verbose_name='titre')
    description = models.TextField(max_length=2048, blank=True, verbose_name="description")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_tickets')
    image = models.ImageField(null=True, blank=True, verbose_name='image')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='uploaded_tickets')
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
