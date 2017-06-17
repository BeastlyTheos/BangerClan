from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms


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
