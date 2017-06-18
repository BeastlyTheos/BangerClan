from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms


def register(request):
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = forms.PlayerCreationForm( request.POST)
		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			form.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/')

	# If this is a GET (or any other method) create the default form.
	else:
		form = forms.PlayerCreationForm()
	context = {"form": form}
	return render( request, "player/register.html", context)
