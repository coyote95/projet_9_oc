from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from authentication.models import User, UserFollows
from django.contrib import messages
from django.http import HttpResponseForbidden
from . import forms
from . import models
import logging
from django.db.models import Q
from itertools import chain

logger = logging.getLogger(__name__)


def home(request):
    following_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    tickets = models.Ticket.objects.filter(Q(user__in=following_users) | Q(user=request.user)).distinct()
    reviews = (models.Review.objects.filter(Q(user__in=following_users) | Q(user=request.user) | Q(ticket__user=
                                                                                                   request.user)).distinct())
    tickets_and_reviews = sorted(
        chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)

    context = {
        'tickets_and_reviews': tickets_and_reviews,
    }
    return render(request, 'blog/home.html', context=context)


def posts(request):
    tickets = models.Ticket.objects.filter(user=request.user).distinct()
    reviews = (models.Review.objects.filter(Q(user=request.user)).distinct())
    tickets_and_reviews = sorted(
        chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)

    context = {
        'tickets_and_reviews': tickets_and_reviews,
    }
    return render(request, 'blog/posts.html', context=context)


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
def review_edit(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)

    if request.user != review.user:
        return redirect('posts')

    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = forms.ReviewForm(instance=review)

    return render(request, 'blog/review_edit.html', {'form': form, 'review': review})


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)

    if request.user != review.user:
        return redirect('posts')

    if request.method == 'POST':
        delete_form = forms.DeleteReviewForm(request.POST)
        if delete_form.is_valid():
            review.delete()
            return redirect('posts')
    else:
        delete_form = forms.DeleteReviewForm()

    context = {
        'review': review,
        'delete_form': delete_form,
    }

    return render(request, 'blog/review_delete.html', context)


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

    if request.method == "POST":
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts')
    return render(request, 'blog/edit_ticket.html', {'edit_form': edit_form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect('posts')

    if request.method == "POST":
        delete_form = forms.DeleteTicketForm(request.POST)
        if delete_form.is_valid():
            ticket.delete()
            return redirect('posts')
    else:
        delete_form = forms.DeleteTicketForm()

    context = {
        'ticket': ticket,
        'delete_form': delete_form,
    }
    return render(request, 'blog/delete_ticket.html', context)


@login_required
def subscribe(request):
    current_user = request.user  # Ou utilisez la logique appropriée pour obtenir l'utilisateur actuel

    if request.method == 'POST':
        form = forms.UserFollowsForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            # Essayez de récupérer l'utilisateur ou renvoyez une réponse 404 personnalisée
            try:
                user_to_follow = User.objects.get(username=username)

                # Vérifiez si la relation d'abonnement n'existe pas déjà
                if user_to_follow == current_user:
                    form.add_error('username', "Vous ne pouvez pas vous abonner à vous-même.")
                elif not UserFollows.objects.filter(user=current_user, followed_user=user_to_follow).exists():
                    UserFollows.objects.create(user=current_user, followed_user=user_to_follow)
                    return redirect('subscribe')  # Redirigez vers la page suivante après l'abonnement
                else:
                    form.add_error('username', "Vous êtes déjà abonné à cet utilisateur.")
            except User.DoesNotExist:
                form.add_error('username', "L'utilisateur n'existe pas.")

    else:
        form = forms.UserFollowsForm()

        # Récupérez les personnes auxquelles l'utilisateur est abonné
    following = UserFollows.objects.filter(user=current_user).values_list('followed_user__username', flat=True)

    # Récupérez les personnes abonnées à l'utilisateur
    followers = UserFollows.objects.filter(followed_user=current_user).values_list('user__username', flat=True)

    return render(request, 'blog/subscribe.html', {'form': form, 'following': following, 'followers': followers})


@login_required
def unsubscribe(request):
    if request.method == 'POST':
        current_user = request.user
        unfollow_username = request.POST.get('unfollow_username', None)

        if unfollow_username:
            try:
                user_to_unfollow = User.objects.get(username=unfollow_username)

                # Vérifiez si l'utilisateur actuel est le propriétaire du compte à désabonner
                if user_to_unfollow != current_user:
                    UserFollows.objects.filter(user=current_user, followed_user=user_to_unfollow).delete()
                    messages.success(request, f"Vous vous êtes désabonné de {unfollow_username}.")
                else:
                    return HttpResponseForbidden("Vous ne pouvez pas vous désabonner de vous-même.")
            except User.DoesNotExist:
                messages.error(request, "L'utilisateur n'existe pas.")

    return redirect('subscribe')
