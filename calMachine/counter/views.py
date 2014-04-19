from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from counter.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse


""" index page view info. """
def index(request):
	context =RequestContext(request)

	context_dict = {'boldmessage': " "}
	return render_to_response('counter/index.html', context_dict, context)


""" register view info """
def register(request):
	context = RequestContext(request)
	
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request. Files:
				profile.picture = request.Files['picture']

			profile.save()

			registered = True
		else:	
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
		'counter/register.html',
		{'user_form': user_form, 'profile_form':profile_form, 'registered':registered},
		context)


""" login veiw code"""

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':

		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password )

		if user is not None:
            # Is the account active? It could have been disabled.
			if user.is_active:
               
				login(request, user)
				return HttpResponseRedirect('/counter/')
			else:
				return HttpResponse("Your Hit The Mark account is disabled.")

		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render_to_response('counter/login.html', {}, context)


