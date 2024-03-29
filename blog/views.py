"""
This module defines Django views.

   - home(request): Displays the home page with tickets and reviews from followed users.
    - posts(request): Displays posts (tickets and reviews) created by the logged-in user.
    - review_create(request, ticket_id): Creates a new review for a specific ticket.
    - review_edit(request, review_id): Edits an existing review created by the logged-in user.
    - review_delete(request, review_id): Deletes an existing review created by the logged-in user.
    - ticket_create(request): Creates a new ticket.
    - ticket_request(request): Creates a new ticket of type 'REQUEST'.
    - ticket_edit(request, ticket_id): Edits an existing ticket created by the logged-in user.
    - ticket_delete(request, ticket_id): Deletes an existing ticket created by the logged-in user.
    - ticket_and_review(request): Creates a new ticket and an associated review.
    - subscribe(request): Handles user subscriptions.
    - unsubscribe(request): Handles user unsubscriptions.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from authentication.models import User, UserFollows
from django.contrib import messages
from django.http import HttpResponseForbidden
from . import forms
from . import models
from django.db.models import Q
from itertools import chain


@login_required
def home(request):
    """
        Renders the home page (flux) displaying tickets and reviews from followed users.

    Retrieves tickets and reviews from followed users and the current user, sorts them by creation time,
    and renders the home page with the obtained data.
    """
    following_users = UserFollows.objects.filter(user=request.user).values_list("followed_user", flat=True)
    tickets = models.Ticket.objects.filter(Q(user__in=following_users) | Q(user=request.user)).distinct()
    reviews = models.Review.objects.filter(
        Q(user__in=following_users) | Q(user=request.user) | Q(ticket__user=request.user)
    ).distinct()
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created,
                                 reverse=True)

    for instance in tickets_and_reviews:
        if isinstance(instance, models.Ticket):  # Only check reviews for Ticket instances
            instance.user_has_reviewed_ticket = models.Review.objects.filter(
                user=request.user, ticket=instance
            ).exists()
    context = {
        "tickets_and_reviews": tickets_and_reviews,
    }
    return render(request, "blog/home.html", context=context)


@login_required
def posts(request):
    """
     Renders the posts page displaying tickets and reviews created by the logged-in user.

    Retrieves tickets and reviews created by the logged-in user, sorts them by creation time,
    and renders the posts page with the obtained data.

    """
    tickets = models.Ticket.objects.filter(user=request.user).distinct()
    reviews = models.Review.objects.filter(Q(user=request.user)).distinct()
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created,
                                 reverse=True)

    context = {
        "tickets_and_reviews": tickets_and_reviews,
    }
    return render(request, "blog/posts.html", context=context)


@login_required
def review_create(request, ticket_id):
    """
    Handles the creation of a new review for a specific ticket.

    If the user already has a review for the ticket, redirects to the home page.
    If the form is submitted with valid data, creates a new review associated with the ticket
    and redirects to the home page.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    existing_review = models.Review.objects.filter(user=request.user, ticket=ticket).first()
    if existing_review:
        return redirect("home")
    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("home")
    else:
        form = forms.ReviewForm()
    return render(request, "blog/review_create.html", {"form": form, "ticket": ticket})


@login_required
def review_edit(request, review_id):
    """
     Handles the editing of an existing review created by the logged-in user.

    If the user is not the owner of the review, redirects to the posts page.
    If the form is submitted with valid data, updates the review and redirects to the posts page.
    """
    review = get_object_or_404(models.Review, id=review_id)
    if request.user != review.user:
        return redirect("posts")
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = forms.ReviewForm(instance=review)
    return render(request, "blog/review_edit.html", {"form": form, "review": review})


@login_required
def review_delete(request, review_id):
    """
    Handles the deletion of an existing review created by the logged-in user.

    If the user is not the owner of the review, redirects to the posts page.
    If the form is submitted with valid data, deletes the review and redirects to the posts page.
    """
    review = get_object_or_404(models.Review, id=review_id)
    if request.user != review.user:
        return redirect("posts")
    if request.method == "POST":
        delete_form = forms.DeleteReviewForm(request.POST)
        if delete_form.is_valid():
            review.delete()
            return redirect("posts")
    else:
        delete_form = forms.DeleteReviewForm()

    context = {
        "review": review,
        "delete_form": delete_form,
    }
    return render(request, "blog/review_delete.html", context)


@login_required
def ticket_create(request):
    """
    Handles the creation of a new ticket.

    If the form is submitted with valid data, creates a new ticket and redirects to the home page.

    """
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            if not ticket.image:
                ticket.image = "none.png"
            ticket.user = request.user
            ticket.uploader = request.user
            ticket.ticket_type = "CREATED"
            ticket.save()
            return redirect("home")
    else:
        form = forms.TicketForm()
    return render(request, "blog/ticket_create.html", {"form": form})


@login_required
def ticket_request(request):
    """
     Handles the creation of a new ticket of type 'REQUEST'.

    If the form is submitted with valid data, creates a new ticket of type 'REQUEST' and redirects to the home page.
    """
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            if not ticket.image:
                ticket.image = "none.png"
            ticket.user = request.user
            ticket.uploader = request.user
            ticket.ticket_type = "REQUEST"
            ticket.save()
            return redirect("home")
    else:
        form = forms.TicketForm()
    return render(request, "blog/ticket_request.html", {"form": form})


@login_required
def ticket_edit(request, ticket_id):
    """
    Handles the editing of an existing ticket created by the logged-in user.

    If the user is not the owner of the ticket, redirects to the home page.
    If the form is submitted with valid data, updates the ticket and redirects to the posts page.

    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect("home")
    if request.method == "POST":
        edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            ticket = edit_form.save(commit=False)
            if "image-clear" in request.POST:
                ticket.image = "none.png"
            elif "image" in request.FILES:
                # Update 'image' if a new file is provided
                ticket.image = request.FILES["image"]
            ticket.save()
            return redirect("posts")
    else:
        edit_form = forms.TicketForm(instance=ticket)
    return render(request, "blog/ticket_edit.html", {"edit_form": edit_form, "ticket": ticket})


@login_required
def ticket_delete(request, ticket_id):
    """
    Handles the deletion of an existing ticket created by the logged-in user.

    If the user is not the owner of the ticket, redirects to the posts page.
    If the form is submitted with valid data, deletes the ticket and redirects to the posts page.
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.user != ticket.user:
        return redirect("posts")
    if request.method == "POST":
        delete_form = forms.DeleteTicketForm(request.POST)
        if delete_form.is_valid():
            ticket.delete()
            return redirect("posts")
    else:
        delete_form = forms.DeleteTicketForm()

    context = {
        "ticket": ticket,
        "delete_form": delete_form,
    }
    return render(request, "blog/ticket_delete.html", context)


@login_required
def ticket_and_review(request):
    """
    Handles the creation of a new ticket and an associated review.

    If the forms are submitted with valid data, creates a new ticket and an associated review,
    and redirects to the home page.
    """
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            if not ticket.image:
                ticket.image = "none.png"
            ticket.user = request.user
            ticket.uploader = request.user
            ticket.ticket_type = "CREATED"
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.headline = ticket.title
            review.user = request.user
            review.save()
            return redirect("home")
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }
    return render(request, "blog/ticket_and_review_create.html", context)


@login_required
def subscribe(request):
    """
     Handles user subscriptions to other users.

    If the form is submitted with valid data, subscribes the user to another user and redirects to the subscribe page.
    """
    current_user = request.user
    if request.method == "POST":
        form = forms.UserFollowsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            try:
                user_to_follow = User.objects.get(username=username)
                if user_to_follow == current_user:
                    form.add_error("username", "Vous ne pouvez pas vous abonner à vous-même.")
                elif not UserFollows.objects.filter(user=current_user, followed_user=user_to_follow).exists():
                    UserFollows.objects.create(user=current_user, followed_user=user_to_follow)
                    return redirect("subscribe")  # Redirigez vers la page suivante après l'abonnement
                else:
                    form.add_error("username", "Vous êtes déjà abonné à cet utilisateur.")
            except User.DoesNotExist:
                form.add_error("username", "L'utilisateur n'existe pas.")
    else:
        form = forms.UserFollowsForm()
    following = UserFollows.objects.filter(user=current_user).values_list("followed_user__username", flat=True)
    followers = UserFollows.objects.filter(followed_user=current_user).values_list("user__username", flat=True)
    return render(request, "blog/subscribe.html", {"form": form, "following": following,
                                                   "followers": followers})


@login_required
def unsubscribe(request):
    """
    Handles user unsubscriptions from other users.

    If the form is submitted with valid data, unsubscribes the user from another user and redirects to the
    subscribe page.
    If the user attempts to unsubscribe from themselves, returns an HttpResponseForbidden.
    If the target user does not exist, displays an error message.
    """
    if request.method == "POST":
        current_user = request.user
        unfollow_username = request.POST.get("unfollow_username", None)
        if unfollow_username:
            try:
                user_to_unfollow = User.objects.get(username=unfollow_username)
                if user_to_unfollow != current_user:
                    UserFollows.objects.filter(user=current_user, followed_user=user_to_unfollow).delete()
                    messages.success(request, f"Vous vous êtes désabonné de {unfollow_username}.")
                else:
                    return HttpResponseForbidden("Vous ne pouvez pas vous désabonner de vous-même.")
            except User.DoesNotExist:
                messages.error(request, "L'utilisateur n'existe pas.")
    return redirect("subscribe")
