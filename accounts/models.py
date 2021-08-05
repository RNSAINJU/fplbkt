from django.db import models
from django.contrib.auth.models import  User
from django.db.models.signals import post_save
from django.dispatch import receiver
from fplengine.models import Teams, Winner
import os
import random

# def get_filename_ext(filepath):
#     base_name=os.path.basename(filepath)
#     name,ext=os.path.splitext(base_name)
#     return name,ext

# def user_image_path(instance, filename):
#     new_filename=random.randint(1,1234567890)
#     name,ext=get_filename_ext(filename)
#     final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
#     return "userprofile/{final_filename}".format(
#         new_filename=new_filename,
#         final_filename=final_filename
#     )

# class Profile(models.Model):
#     STATUS_CHOICES=(
#     ('active','Active'),
#     ('in-active','In-active'),
#     )
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     # name=models.CharField(max_length=30,unique=True)
#     address=models.CharField(max_length=40)
#     phone_no=models.IntegerField(null=True)
#     short_description=models.CharField(max_length=80, unique=True)
#     description=models.TextField(unique=True)
#     description2=models.TextField(unique=True,blank=True)
#     name_in_style= models.CharField(max_length=30, unique=True)
#     image1=models.ImageField(upload_to=user_image_path, null=True, blank=False)
#     fb_link=models.CharField(max_length=100, unique=True)
#     teams=models.ManyToManyField(Teams)
#     # winner=models.OneToOneField(Winner, on_delete=models.CASCADE)
#     rewards=models.ImageField(upload_to=user_image_path, null=True, blank=True)
#     # collection=models.ManyToManyField(Teams)

#     def __str__(self):
#         return self.user.username

# @receiver(post_save,sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()