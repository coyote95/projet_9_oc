from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from authentication.models import User, UserFollows
from . import forms
from . import models
import logging

logger = logging.getLogger(__name__)


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(request, 'blog/home.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def review_create(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = forms.ReviewForm()

    return render(request, 'blog/review_create.html', {'form': form, 'ticket': ticket})


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.uploader = request.user
            ticket.ticket_type = 'CREATED'
            ticket.save()
            return redirect('home')
    else:
        form = forms.TicketForm()

    return render(request, 'blog/ticket_create.html', {'form': form})


def ticket_request(request):
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.uploader = request.user
            ticket.ticket_type = 'REQUEST'
            ticket.save()
            return redirect('home')
    else:
        form = forms.TicketForm()

    return render(request, 'blog/ticket_request.html', {'form': form})


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'blog/view_ticket.html', {'ticket': ticket})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect('home')
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == "POST":
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_ticket.html', context=context)


@login_required
def subscribe(request):
    if request.method == 'POST':
        form = forms.UserFollowsForm(request.POST)
        current_user = request.user  # Ou utilisez la logique appropriée pour obtenir l'utilisateur actuel

        if form.is_valid():
            username = form.cleaned_data['username']

            # Essayez de récupérer l'utilisateur ou renvoyez une réponse 404 personnalisée
            try:
                user_to_follow = User.objects.get(username=username)

                # Vérifiez si la relation d'abonnement n'existe pas déjà
                if not UserFollows.objects.filter(user=current_user, followed_user=user_to_follow).exists():
                    UserFollows.objects.create(user=current_user, followed_user=user_to_follow)
                    return redirect('home')  # Redirigez vers la page suivante après l'abonnement
                else:
                    form.add_error('username', "Vous êtes déjà abonné à cet utilisateur.")

            except User.DoesNotExist:
                form.add_error('username', "L'utilisateur n'existe pas.")

    else:
        form = forms.UserFollowsForm()

    return render(request, 'blog/subscribe.html', {'form': form})