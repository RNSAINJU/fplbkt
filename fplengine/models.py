from django.db import models
from django.conf import settings
import os
import random
from django.shortcuts import render, get_object_or_404

def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext

def user_image_path(instance, filename):
    new_filename=random.randint(1,1234567890)
    name,ext=get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "company/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

def winner_image_path(instance, filename):
    new_filename=random.randint(1,123456789)
    name, ext=get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "winner/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class Division(models.Model):
    name=models.CharField(max_length=10, unique=True, blank=True)

    def __str__(self):
        return self.name


class Teams(models.Model):
    ACTIVE_CHOICES=(
        ('eliminated','Eliminated'),
        ('not eliminated','Not eliminated'),
    )
    SAFE_CHOICES=(
        ('safe','Safe'),
        ('not safe','Not safe'),
    )
    name=models.CharField(max_length=30)
    teamname=models.CharField(max_length=30)
    entry=models.IntegerField(unique=True)
    divisions=models.ForeignKey(Division, on_delete=models.CASCADE, blank=True, null=True)
    elimination=models.CharField(max_length=30,choices=ACTIVE_CHOICES,default='not eliminated')
    # eliminatedgameweek=models.ForeignKey(Gameweek,on_delete=models.CASCADE, blank=True, null=True)
    eliminatedwithpoints=models.IntegerField(blank=True, null=True)
    # iamsafeliminatedgameweek=models.ForeignKey(IamSafe,on_delete=models.CASCADE, blank=True, null=True)
    issafe=models.CharField(max_length=30,choices=SAFE_CHOICES,default='safe')
    iamsafeoutpoints=models.IntegerField(blank=True, null=True)
    eliminated_gameweek=models.PositiveIntegerField(null=True, blank=True)

    date=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     division=Division.objects.all()
    #     for div in division.all:
    #         self.divisions='active'
    #     super(Gameweekwinner,self).save(*args,**kwargs)

    





# This model is for user every gameweek point
class Gameweek(models.Model):
    no=models.IntegerField(unique=False,blank=True, null=True)
    player=models.ForeignKey(Teams,on_delete=models.CASCADE, blank=True, null=True)
    point=models.IntegerField(unique=False,blank=True, null=True)
    point_on_bench=models.IntegerField(unique=False,blank=True, null=True)
    totalpoints=models.IntegerField(unique=False,blank=True, null=True)
    bank=models.FloatField(unique=False,blank=True, null=True)
    value=models.FloatField(unique=False,blank=True, null=True)
    event_transfers=models.IntegerField(unique=False,blank=True, null=True)
    event_transfers_cost=models.IntegerField(unique=False,blank=True, null=True)

    def __str__(self):
        if self.player:
            return "Gameweek-"+str(self.no)+self.player.name
        return "Gameweek"+str(self.no)

class IamSafe(models.Model):
    safemargin=models.IntegerField(unique=False,blank=False)
    gameweek=models.IntegerField()

    def __str__(self):
        return str(self.gameweek)

class Company(models.Model):
    STATUS_CHOICES=(
    ('active','Active'),
    ('in-active','In-active'),
    )
    name=models.CharField(max_length=30,unique=True)
    address=models.CharField(max_length=40)
    phone_no=models.IntegerField(null=True)
    short_description=models.CharField(max_length=80, unique=True)
    description=models.TextField(unique=True)
    description2=models.TextField(unique=True,blank=True)
    name_in_style= models.CharField(max_length=30, unique=True)
    logo=models.ImageField(upload_to=user_image_path, null=True, blank=False)
    image1=models.ImageField(upload_to=user_image_path, null=True, blank=True)
    # image2=models.ImageField(upload_to=user_image_path, null=True, blank=True)
    rules1=models.ImageField(upload_to=user_image_path, null=True, blank=True)
    rules2=models.ImageField(upload_to=user_image_path, null=True, blank=True)
    gameweek_winner_description=models.TextField()
    classic_league_description=models.TextField()
    division_description=models.TextField()
    elimination_description=models.TextField()
    elimination_image=models.ImageField(upload_to=user_image_path, null=True, blank=True)
    iamsafe_description=models.TextField()
    iamsafe_image=models.ImageField(upload_to=user_image_path, null=True, blank=True)
    fb_link=models.CharField(max_length=100, unique=True)
    rewards=models.ImageField(upload_to=user_image_path, null=True, blank=True)


    def __str__(self):
        return self.name




class ClassicLeague(models.Model):
    position=models.IntegerField()
    name=models.OneToOneField(Teams,on_delete=models.CASCADE,null=True,blank=True)
    event_total= models.PositiveIntegerField(null=True, blank=True)
    total_points=models.IntegerField(null=True,blank=True)
    reward=models.CharField(max_length=20)

    def __str__(self):
        return str(self.position)

class DivisionLeague(models.Model):
    position=models.IntegerField(unique=True)
    name=models.OneToOneField(Teams,on_delete=models.CASCADE,null=True,blank=True)
    event_total= models.PositiveIntegerField(null=True, blank=True)
    total_points=models.IntegerField(null=True,blank=True)
    reward=models.CharField(max_length=20)
    # divisions=models.ForeignKey(Division,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return "Division-"+self.name.divisions.name+str(self.position)


class Gameweekwinner(models.Model):
    STATUS_CHOICES=(
    ('active','Active'),
    ('in-active','In-active')
    )
    name=models.ManyToManyField(Teams)
    gameweek=models.PositiveIntegerField()
    points=models.IntegerField(blank=False)
    activeinhome=models.CharField(max_length=30,choices=STATUS_CHOICES,default='in-active')

    def __str__(self):
        return str(self.gameweek)
    
    # def save(self, *args, **kwargs):
    #     gwwinner=Gameweekwinner.objects.filter(activeinhome='active')
    #     self.activeinhome='active'
    #     super(Gameweekwinner,self).save(*args,**kwargs)


class DivisionGameweekWinner(models.Model):
    name=models.ForeignKey(Teams,on_delete=models.CASCADE, blank=True, null=True)
    gameweek=models.PositiveIntegerField()
    points=models.IntegerField()

    def __str__(self):
        return "Division-" + self.team.divisions.name + "-" +"Gameweek" + str(self.gameweek) + "-Winner"

    

class Winner(models.Model):
    name=models.OneToOneField(Teams,on_delete=models.CASCADE)
    Year=models.IntegerField(unique=True,blank=False)
    image=models.ImageField(upload_to=winner_image_path,null=True,blank=False)
    points=models.IntegerField(unique=True,blank=False)
    voice=models.TextField(unique=True,blank=False)

    def __str__(self):
        return self.name.name

# class Collection(models.Model):
#     FEATURED_CHOICES=(
#         ('yes','Yes'),
#         ('no','No'),
#     )
#     # user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     name=models.CharField(max_length=30, unique=True)
#     short_description=models.CharField(max_length=80, unique=True)
#     image=models.ImageField(upload_to=users_image_path,null=True,blank=False)
#     featured=models.CharField(max_length=10,choices=FEATURED_CHOICES,default='no')
#     date=models.DateTimeField(auto_now_add=True,blank=True)

#     def __str__(self):
#         return self.name