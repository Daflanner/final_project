from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from counter.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import date


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
			

			profile = profile_form.save(commit=False)
			profile.user = user

			#if 'picture' in request.Files:
			#	profile.picture = request.Files['picture']

			profile.save()
			user.save()

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
				return HttpResponseRedirect('/counter/Day_Record/')
			else:
				return HttpResponse("Your Hit The Mark account is disabled.")

		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render_to_response('counter/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    
    # Take the user back to the homepage.
    return HttpResponseRedirect('/counter/')



""" Recorded days Page"""

from counter.forms import RecordedDays
from django.contrib.auth.decorators import login_required
@login_required

def Day_Record(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = RecordedDays(request.POST)

		if form.is_valid():
			try: 
				record = RecordedDays.objects.get(userprofile= request.user.userprofile, Date = form.date)
			except:
				
				record = form.save(commit=False)
				record.profile = request.user.userprofile
				record.save()


			return HttpResponseRedirect('/counter/' + str(record.Date) +'/')


		else: 
			print form.errors

	else:

		form = RecordedDays()

	return render_to_response('counter/Day_Record.html', {'form':form}, context)


""" Meal type page """
from counter.forms import MealType
from django.contrib.auth.decorators import login_required
@login_required


def MealEntry(request,year, month, day):
	context = RequestContext(request)
    
	if request.method == 'POST':
		form = MealType(request.POST)

		if form.is_valid():
			
			record = form.save(commit=False)
			record.Date = datetime
			record.save()


			return HttpResponseRedirect('/counter/Component')

		else: 
			print form.errors

	else:

		form = MealType()

	return render_to_response('counter/MealEntry.html', {'form':form}, context)

"""  Ingredient Page """

from counter.forms import Ingredient
from django.contrib.auth.decorators import login_required
@login_required


def Component(request):
	context = RequestContext(request)
    
	if request.method == 'POST':
		form = Ingredient(request.POST)

		if form.is_valid():
			
			record = form.save(commit=False)
			record = request.RecordedDays
			record.save()


			return HttpResponseRedirect('/counter/Component')

		else: 
			print form.errors

	else:

		form = Ingredient()

	return render_to_response('counter/Ingredients.html', {'form':form}, context)





