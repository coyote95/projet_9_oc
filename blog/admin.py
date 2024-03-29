"""
This module configures the Django Admin interface .

Admin Classes:
    - TicketsAdmin: Customizes the display of Ticket model with ('title', 'description', 'user', 'time_created').
    - ReviewsAdmin: Customizes the display of Review model with ('ticket', 'rating', 'user', 'headline', 'body',
     'time_created')
    - UserFollowsAdmin: Customizes the display of UserFollows model with('user', 'followed_user')

"""


from django.contrib import admin
from blog.models import Ticket, Review
from authentication.models import UserFollows


class TicketsAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "user", "time_created")


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("ticket", "rating", "user", "headline", "body", "time_created")


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")


admin.site.register(Ticket, TicketsAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
