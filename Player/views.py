from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from . import forms
from .models import Player, Char, PendingCharRegistration


def register(request):
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = forms.PlayerCreationForm( request.POST)
		# Check if the form is valid:
		if form.is_valid():
			form.save()
			# redirect to the confirmation page
			context = {"email":request.POST['email'], "initial_char":request.POST['initial_char']}
			return render( request, "player/registration_confirmation.html", context)

	# If this is a GET (or any other method) create the default form.
	else:
		form = forms.PlayerCreationForm()
	context = {"form": form}
	return render( request, "player/register.html", context)


def request_char(request):
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = forms.RequestCharForm( request.POST)
		# Check if the form is valid:
		if form.is_valid():
			form.save(request.user)
			# redirect to the confirmation page
			context = {"char":form.cleaned_data["char"]}
			return render( request, "player/request_char_confirmation.html", context)

	# If this is a GET (or any other method) create the default form.
	else:
		form = forms.RequestCharForm()
	context = {"form": form}
	return render( request, "player/request_char.html", context)


def ShowPendingChars(request):
	chars = PendingCharRegistration.objects.all()
	html = "<title>pendings</title><table>"
	for char in chars:
		url = "http://{0}{1}?token={2}".format(get_current_site(request), reverse("register_char"), char.token)
		html = html + "<tr><td>{0}</td><td>{1}</td><td> <a href='{2}'>{2}</a> </td></tr>".format(char.player.email, char.name, url)
	return HttpResponse( html)

def register_char(request):
	try:
		token = request.GET.get("token")
		pending_char = PendingCharRegistration.objects.get(token=token)
	except Exception:
		return render(request, "player/register_char_error.html", {"msg":"invalid or missing token. Please insure that the complete url has been copied from mume and try again."})

	if Char.objects.filter(name=pending_char.name).exists():
		if Char.objects.get(name=pending_char.name).owner.id == pending_char.player.id:
			return render(request, "player/register_char_error.html", {"msg":"It appears you have already registered this char to your account"})
		else:
			return render(request, "player/register_char_error.html", {"msg":"It appears somebody else has already registered this char to their account. If you think this is in error, please contact the site admins"})

	char = Char(owner=pending_char.player, name=pending_char.name)
	char.save()
	char.owner.current_char = char
	char.owner.save()
	pending_char.delete()
	context = {"email":char.owner.email, "char":char.name}
	return render(request, "player/register_char_confirmation.html", context)

@login_required
def profile(request):
	context = {"user": request.user}
	return render(request, "player/profile.html", context)
