from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from counter.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import RecordedDays,MealType,Ingredient


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
            #   profile.picture = request.Files['picture']

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

from counter.forms import RecordedDaysFRM
from django.contrib.auth.decorators import login_required
@login_required

def Day_Record(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = RecordedDaysFRM(request.POST)

        if form.is_valid():
            try: 
                record = RecordedDays.objects.get(
                    profile= request.user.userprofile, 
                    Date = form.cleaned_data['Date'])
            
            except Exception as Datefail:       #creates meal object from drop down field. 
                print type( Datefail)
                print Datefail.args
                
                record = form.save(commit=False)
                record.profile = request.user.userprofile
                record.save()

                #puts yr, month, day into URL w/ form submission
            return HttpResponseRedirect('/counter/' + str(record.Date) +'/')


        else: 
            print form.errors

    else:

        form = RecordedDaysFRM()

    return render_to_response('counter/Day_Record.html', {'form':form}, context)


""" Meal type page """
from counter.forms import MealTypeFRM
from django.contrib.auth.decorators import login_required
@login_required


def MealEntry(request,year, month, day):
    #url.py calls mealEntry view with yr month and Day extracted  from recordeddate URL


    context = RequestContext(request)
    context["recorddate"] = "%s-%s-%s" % (year,month, day)
    
    if request.method == 'POST':
        #request is a post, process submited form 
        #instantiate form w/ post data 
        form = MealTypeFRM(request.POST)

        if form.is_valid():
            #if all form fields are valid, process data 

            try:
                
                meal = MealType.objects.get(newDay__profile= request.user.userprofile,
                newDay__Date =date( int(year), int(month), int(day)),
                mealNum =form.cleaned_data['mealNum'])
                

                print "try fully run" 

            except Exception as mealfail:       #creates meal object from drop down field. 
                print type( mealfail)
                print mealfail.args
                
                meal = form.save(commit=False) #but, does not save yet!
            
                        # get method searching RecordedDays class filtering via user profile and date ::: pulls current user profile from the request
            # using date from datetime function to compare against the Date object  from the recordedDays class. 
                meal.newDay = RecordedDays.objects.get(profile= request.user.userprofile, 
                Date = date( int(year), int(month), int(day)  ) )
              
            #Now that the recordedDays has been attatched to meal. The meal record is saved.
                meal.save()

                print "except completed"    

            return HttpResponseRedirect('/counter/%s-%s-%s/%s/' %(year,month,day,meal.mealNum))

        else: 
            print form.errors

    else:
         
        form = MealTypeFRM()

    return render_to_response('counter/MealEntry.html', {'form':form}, context)

"""  Ingredient Page """

from counter.forms import IngredientFRM
from django.contrib.auth.decorators import login_required
@login_required


def Component(request,year, month, day,mealtp):#url parser grabs these parameters from the URL bar
    context = RequestContext(request)
    mealTP_dict= {   # tranlates the 2 letter code for a meal from the URL bar into the the full word for the meal 
       'BF':'Breakfast',
       'LN': 'Lunch',
       'DN': 'Dinner',
       'SN': 'Snack'}
    context['mealText'] = mealTP_dict[mealtp] #creates meal text object for tmeplate
    context['mealDate'] = '%s-%s-%s' %(year,month,day) #creates a meal date object for template
    context[ 'MealType'] = mealtp #creates "MealType" object to be put in the URL


            # .filter returns a list or nothing. While .get return one item or nothing

            #   .objects is the object mananager and filter returns a list based on the queery parameters. 

#  A__ B means roughly "Search A Where it is attatched to B"
    context[ 'comp_list'] = Ingredient.objects.filter(numMeal__newDay__profile= request.user.userprofile, 
                                        #search ingredient objects where the numMeal(fk)is points to the newDay(fk) that points to the profile(fk) 
                                        #that matches the user profile of the request.
                                         
        numMeal__newDay__Date= date( int(year),  int(month), int(day)   ),numMeal__mealNum=mealtp )         
            

            #searches through the models to get the right meal for the right day in the profile.
            #projects it to the template.. 
    context[ 'current_meal'] = MealType.objects.get(newDay__profile = request.user.userprofile, 
        newDay__Date= date( int(year),  int(month), int(day) ), mealNum = mealtp )


    if request.method == 'POST':
        form = IngredientFRM(request.POST)

        if form.is_valid():
            
            Component =  form.save(commit=False)   
            Component.numMeal = MealType.objects.get(newDay__profile= request.user.userprofile, 
            newDay__Date= date( int(year), int(month), int(day) ),mealNum=mealtp )          
            
            Component.save()

            return HttpResponseRedirect('/counter/%s-%s-%s/%s/' %(year,month,day,mealtp))

        else: 
            print form.errors

    else:
        form = IngredientFRM()

    return render_to_response('counter/Ingredients.html', {'form':form}, context)



"""" Day_view Code """

def Day_view(request, year, month, day ):
    context = RequestContext(request)
    
#Pulling the Date out of the URL. Creating separate year, month and Day variables
#So that they can be put in any order in the template
    context['year'] = '%s' %(year,) 
    context['month'] = '%s' %(month,)   
    context['day'] = '%s' % (day,)  

# Creating empty list Day_food
    day_food =[ ]

#creating Meal_list using object filter sorting via foreign keys.
    meal_list = MealType.objects.filter(newDay__profile = request.user.userprofile, 
        newDay__Date= date( int(year),  int(month), int(day) ) )
    
#filling the empty day food list such that the meal title is the zeroeth element 
        #of the list and the meal total is the 1st. 
    for meal in meal_list:
        day_food.append( [ meal.get_mealNum_display(), meal.Mealtotal()  ]  )
                    #.get_mealNum_display() translates 2 ltr code to word for meal
        
        comp_list =Ingredient.objects.filter(numMeal = meal)
        

        for comp in comp_list:
            day_food[-1].append([comp.component, comp.comp_total()] )
                #

#Creating Day food and Meal_list variables to be called by template.
    context['day_food'] = day_food
    context['meal_list'] = meal_list
    context['comp_list'] = comp_list


    #return HttpResponseRedirect('/counter/%s-%s-%s/%s/' %(year,month,day)'/Day_view)'
    return render_to_response('counter/Day_view.html', context)


""" History view code """

from counter.forms import Date_rangeFRM
from django.contrib.auth.decorators import login_required
@login_required

def date_range(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        form = Date_rangeFRM(request.POST)
        print "valid", form.is_valid()
        print "form", str(form)
        if form.is_valid():
            

            Single_date = form.cleaned_data['Single_date']
                #print "form", str(form)
                    
    
            if Single_date and Single_date  != "":
                
                try: 
                    print "try started "
                    record = RecordedDays.objects.get(
                        profile= request.user.userprofile, 
                        Date = form.cleaned_data['Single_date'])
                    print "try executed"
                    return HttpResponseRedirect('/counter/%02d-%02d-%02d/Day_view/' %(Single_date.year,Single_date.month,Single_date.day))
                
 
                except:
                    return HttpResponse("Sorry but you have no data for that date. Please click the back button and enter a different date.")
                    print form.errors
                    print "except executed"

            else:
                            
                Date_start = form.cleaned_data['Date_start']
                Date_end = form.cleaned_data['Date_end']
                # TODO:  Add check for missing either start or end date.
                if not Date_start and not Date_end:
                    return HttpResponse("Sorry must supply either a Single date or a Start and End date pair. Please click the back button and enter a missing date.")
                elif not Date_start:
                    return HttpResponse("Sorry must supply a Start date. Please click the back button and enter a missing date.")
                elif not Date_end:
                    return HttpResponse("Sorry must supply an End date. Please click the back button and enter a missing date.")
                # 
                dt_range = []  
                dt_range_total = 0
                day_list = RecordedDays.objects.filter(
                    profile= request.user.userprofile, 
                    Date__gte = Date_start, Date__lte = Date_end).order_by('Date')
                for day in day_list:
                    this_day = []
                    this_day.append(day.Date)
                    day_total = day.DayTotal()
                    this_day.append(day_total)
                    dt_range_total += day_total
                    meal_list = MealType.objects.filter(
                        newDay__profile = request.user.userprofile, 
                        newDay__Date = day.Date)
                        #newDay__Date__gte = Date_start, newDay__Date__lte = Date_end     )
                    #newDay__Date= date( int(year),  int(month), int(day) ) )

                    for meal in meal_list:
                        this_day.append([ meal.get_mealNum_display(), meal.Mealtotal()  ])
                        comp_list =Ingredient.objects.filter(numMeal = meal)

                        for comp in comp_list:
                            this_day[-1].append([comp.component, comp.comp_total()] ) 



                    #context['meal_list'] = meal_list
                    #context['comp_list'] = comp_list
                    #context['day_list']  = day_list 
                    dt_range.append(this_day)

                #return HttpResponseRedirect('/counter/History_View' (context))
                return render_to_response( 'counter/history_view.html', {'day_list': dt_range, 'dt_range_total': dt_range_total, 'Date_start':Date_start, 'Date_end':Date_end}, context ) 
                

        else: 
            print form.errors

    else:
        form = Date_rangeFRM()  

    return render_to_response('counter/Date_rangeFRM.html', {'form':form}, context)



    



    
        
    

    





