from django.db import models
#AbstractUser to extend default user model
#BaseUserManager to overwrite manager if we want more functionanality
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import datetime

# Create your models here.

#set up a custom user model that can be extended AND used in auth
#dont forget to update AUTH_USER_MODEL to settings.py if we want a diff model
#dont forget to add this model to admin.py if you want admin app access.

class User(AbstractUser, PermissionsMixin):
    email=models.EmailField(unique=True, null=False, blank=False, default="defaultemail@test.com")
    #fields also included inheriting from AbstractUser, PermissionsMixin:
        #username
        #first_name=CharField
        #last_name=CharField
        #is_staff=BooleanField
        #is_active=BooleanField
        #date_joined=DateTimeField
        #password=CharField
        #last_login=DateTimeField
        #is_superuser=BooleanField
        #groups=ManyToManyField
        #user_permissions=ManyToManyField

    #if want to override using 'username' as username field. ex email
    #USERNAME_FIELD =

    #can't set the username_field as a required field
    REQUIRED_FIELDS = ['email', 'password']
    
    def __str__(self):
        return self.username	

#write a custom User manager in order to include hashed passwords 
#and more advanced User features

class UserManager(BaseUserManager):
    pass
    """
        all many to many fields are empty on creation
    """

class MeetupGroup(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=100, default='default description')
    create_date = models.DateField('date created')
    #wow! can avoid circular dependency by specifying associated model class as string. cool. 
    members = models.ManyToManyField('User', related_name='meetup_groups')
    admin = models.ForeignKey(User, null = False, default=1, related_name="admin_user", on_delete=models.CASCADE)

    REQUIRED_FIELDS=['name', 'description','admin']
    
    def __str__(self):
            return self.name

class Tag(models.Model):
    name = models.CharField(max_length=25)
    create_date = models.DateField('date_created')
    meetup_groups = models.ManyToManyField(MeetupGroup, related_name='tags')

    REQUIRED_FIELDS=['name']

    def __str__(self):
            return self.name

class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date = models.DateTimeField('date of event')
    address = models.CharField(max_length = 100)
    date_created = models.DateField('date created')
    host = models.ForeignKey(User, null=False, default=1, related_name='host_user', on_delete=models.CASCADE)
    meetup_group = models.ForeignKey(MeetupGroup, null=False, default=1, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='events')

    REQUIRED_FIELDS=['name','description', 'address', 'host', 'meetup_group']
    
    def __str__(self):
            return self.name
