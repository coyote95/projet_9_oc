from django.contrib import admin
from blog.models import Ticket


class TicketsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'time_created')


admin.site.register(Ticket, TicketsAdmin)
