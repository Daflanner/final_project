from counter.models import UserProfile, RecordedDays, MealType, Ingredient

from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('Calorie_Goal', 'picture')

class RecordedDays(forms.ModelForm):
	
	class Meta:
		model = RecordedDays
		fields = ('Date',)

class MealType (forms.ModelForm):
	
	class Meta:
		model = MealType
		fields = ('mealNum',)

class Ingredient (forms.ModelForm):

	class Meta:
		model = Ingredient
		component = forms.CharField(max_length= 40, help_text ="Please enter the ingredients of the meal quantity for each ingredient, (ex. 2 for 2 slices of bread) and the calories for one unit of that item ")
		Calories = forms.IntegerField(initial = 0)
		Amount = forms.IntegerField(initial = 0)
		comp_total= forms.IntegerField(initial = 0)