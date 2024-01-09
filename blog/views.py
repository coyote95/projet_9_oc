from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
import logging

logger = logging.getLogger(__name__)


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'blog/home.html', context={'tickets': tickets})


@login_required
def ticket_create(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.uploader = request.user
            logger.info(f"Ticket data before save: {ticket.__dict__}")
            ticket.save()
            logger.info(f"Ticket data after save: {ticket.__dict__}")
            return redirect('home')
    return render(request, 'blog/ticket_create.html', context={'form': form})


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'blog/view_ticket.html', {'ticket': ticket})
