"""
This module defines a Django model, UserFollows, to represent the relationship between users
where one user follows another.
"""
from django.db import models
from django.contrib.auth.models import User


class UserFollows(models.Model):
    """
    UserFollows model represents the relationship between users where one user follows another.

    Attributes:
        user: ForeignKey
        followed_user: ForeignKey
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by")

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )
