from django.db import models
from django.contrib.auth.models import User





class UserProfile(models.Model):
    
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    Calorie_Goal = models.IntegerField()


    def __unicode__(self):
        return self.user.username

# Create your models here.
class RecordedDays(models.Model):
    profile = models.ForeignKey(UserProfile, unique = False)
    Date =models.DateField(auto_now=False, auto_now_add =False) 

    def __unicode__(self):
        pass
        return self.profile.user.username

    def DayTotal(self):
        mlist = MealType.object.filter(redordedDay = self)
        DyTotal = 0
        for ml in mlist:
            DyTotal += ml.mlTotal
        return DyTotal


class MealType (models.Model):
    recordedDay = models.ForeignKey(RecordedDays, unique =False)
    mealNum_CHOICES = (
        ('BF','Breakfast'),
        ('LN', 'Lunch'),
        ('DN', 'Dinner')
        )
    mealNum = models.CharField(max_length = 2, 
                                choices = mealNum_CHOICES,
                                default = 'BF',help_text ="Please enter what kind of meal you would like to record")



    def __unicode__(self):
        return self.user.username
    
    def Mealtotal(self):
        ilist = Ingredient.object.filter(numMeal=self)
        mlTotal = 0 
        for ing in ilist: 
            # summation of ingredient totals
            mlTotal += ing.total()
        return mlTotal



class Ingredient (models.Model):
    numMeal = models.ForeignKey(MealType, unique = False)
    ingred = models.CharField(max_length = 40, unique = False)
    ingredNum = models.IntegerField()
    ingCal = models.IntegerField()
	
    def __unicode__(self):
        return self.user.username

    def total(self):
        total = ingredNum * ingCal
        return total