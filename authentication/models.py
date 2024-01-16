from django.db import models
from django.contrib.auth.models import User,AbstractUser


# class User(AbstractUser):
#     follows = models.ManyToManyField(
#         'self',
#         through='UserFollows',
#         symmetrical=False,
#         verbose_name='suit',
#     )
#creer la même table?



class UserFollows(models.Model): #creer une table
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='followed_by')#utilisateur qui est
    # suivi

    class Meta:
        unique_together = ('user', 'followed_user',)
