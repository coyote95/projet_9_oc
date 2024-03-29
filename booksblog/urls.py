"""
URL configuration for booksblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
import authentication.views
import blog.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        LoginView.as_view(template_name="authentication/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("home/", blog.views.home, name="home"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("ticket_review/create/", blog.views.ticket_and_review, name="ticket_and_review_create"),
    path("ticket/create/", blog.views.ticket_create, name="ticket_create"),
    path("ticket/request/", blog.views.ticket_request, name="ticket_request"),
    path("ticket/<int:ticket_id>/edit", blog.views.ticket_edit, name="ticket_edit"),
    path("ticket/<int:ticket_id>/delete/", blog.views.ticket_delete, name="ticket_delete"),
    path("review/<int:ticket_id>/create/", blog.views.review_create, name="review_create"),
    path("review/<int:review_id>/edit/", blog.views.review_edit, name="review_edit"),
    path("review/<int:review_id>/delete/", blog.views.review_delete, name="review_delete"),
    path("subscribe/", blog.views.subscribe, name="subscribe"),
    path("unsubscribe/", blog.views.unsubscribe, name="unsubscribe"),
    path("posts/", blog.views.posts, name="posts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
