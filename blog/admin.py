from django.contrib import admin
from blog.models import Ticket, Review


class TicketsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'time_created')


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'rating', 'user', 'headline', 'body', 'time_created')


admin.site.register(Ticket, TicketsAdmin)
admin.site.register(Review, ReviewsAdmin)
