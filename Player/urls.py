"""Banger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import forms
from . import views


urlpatterns = [
	url(r"^register/", views.register, name="register"),
	url(r"^request_char$", views.request_char, name="request_char"),
	url(r"^show/", views.ShowPendingChars),
	url(r"^register_char$", views.register_char, name="register_char"),
	url(r"^login$", auth_views.login, {"template_name":"player/login.html", "authentication_form":forms.AuthenticationForm}, name="login"),
	url(r"^logout$", auth_views.logout, {"template_name":"player/logged_out.html"}, name="logout"),
	url(r"^password_change$", auth_views.password_change, {"template_name":"player/password_change_form.html"}, name="password_change"),
	url(r"^password_change_done$", auth_views.password_change_done, {"template_name":"player/password_change_done.html"}, name="password_change_done"),
	url(r"^password_reset$", auth_views.password_reset, {"template_name":"player/password_reset.html", "subject_template_name":"player/password_reset_subject.txt", "email_template_name":"player/password_reset_email.html"}, name="password_reset"),
	url(r"^password_reset_done$", auth_views.password_reset_done, {"template_name":"player/password_reset_done.html"}, name="password_reset_done"),
	url(r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", auth_views.password_reset_confirm, {"template_name":"player/password_reset_confirm.html"}, name="password_reset_confirm"),
	url(r"^password_reset_complete$", auth_views.password_reset_complete, {"template_name":"player/password_reset_complete.html"}, name="password_reset_complete"),
	url(r"^profile$", views.profile, name="profile"),
]
