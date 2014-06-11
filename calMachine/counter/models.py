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
        mlist = MealType.objects.filter(redordedDay = self)
        DyTotal = 0
        for ml in mlist:
            DyTotal += ml.mlTotal
        return DyTotal


class MealType (models.Model):
    newDay = models.ForeignKey(RecordedDays, unique =False)
    mealTP_CHOICES= (
       ('BF','Breakfast'),
        ('LN', 'Lunch'),

        
        ('DN', 'Dinner'),
        ('SN', 'Snack'))
        
    mealNum = models.CharField(max_length = 2, 
                                choices = mealTP_CHOICES,
                                default = 'BF',help_text ="Please enter what kind of meal you would like to record")





    def __unicode__(self):
        return str(self.newDay) + self.get_mealNum_display()
    
    def Mealtotal(self):
        ilist = Ingredient.objects.filter(numMeal=self)
        mlTotal = 0 
        for ing in ilist: 
            # summation of ingredient totals
            mlTotal += ing.comp_total()
        return mlTotal


class Ingredient (models.Model):
    numMeal = models.ForeignKey(MealType, unique = False)
    component = models.CharField(max_length = 40, unique = False)
    components_calories = models.IntegerField()
    quantity= models.IntegerField()


    def __unicode__(self):
        return str(self.numMeal) + self.component

    def comp_total(self):
        total = self.quantity *self.components_calories
        return total