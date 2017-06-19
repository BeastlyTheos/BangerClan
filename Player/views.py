from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site

from . import forms
from .models import PendingCharRegistration


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

def ShowPendingChars(request):
	chars = PendingCharRegistration.objects.all()
	html = "<title>pendings</title><table>"
	for char in chars:
		html = html + "<tr><td>{0}</td><td>{1}</td><td> <a href='http://{2}/player/register_char?token={3}'>token</a> </td></tr>".format(char.player.email, char.name, get_current_site(request), char.token)
	return HttpResponse( html)
