from __future__ import annotations
from typing import Union
from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from .models_validation import(
    is_email_address_valid, is_name_valid, is_email_address_valid, 
    is_password_valid
) 
import model_exceptions as me
from ..utils import utils as ut
from django.contrib.auth.models import Permission, Group

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, name, user_name, password, **other_fields):
        if not email:
            raise ValueError(("You must provide an email address"))

        email = self.normalize_email(email)

        user = self.model(
            email=email, name=name, user_name=user_name, **other_fields) 

        if is_password_valid(password):
            password = password.rstrip().lstrip()
            user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, user_name, name, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(
            email=email, user_name=user_name, name=name, password=password,**other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """class to represent a User of the system.
    
    inherits from:
    - AbstractBaseUser
    - PermissionsMixin

    notable fields:
    - name: models.CharField()
    - user_name: models.CharField()
    - email: models.CharField()
    - password: models.CharField()

    self-defined instance methods:
    - get_name_formatted(self) -> str

    self-defined class methods:
    - get_user(cls, email: str, password: str) -> Union[User, None]"""

    name = models.CharField(max_length=40, null=False, blank=False)
    user_name = models.CharField(max_length=40, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=150, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='my_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')
        
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='my_users',
        blank=True,
        help_text='Specific permissions for this user.')



    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'name', 'password']
    
    class Meta:
        ordering = ["name"]

    """ instance methods """

    def get_name_formatted(self) -> str:
        """method to format the name of the user. Capitalization is applied."""
        try:
            splitter = self.name.split(" ")
            return splitter[0].lower().capitalize()
        except:
            return self.name.lower().capitalize()

    def __str__(self):
        try:
            return ut.get_display_name(self.name)
        except:
            return self.name

    def save(self, *args, **kwargs):
        if is_name_valid(self.name):
            self.name = self.name.lower().lstrip().rstrip()
        else:
            raise me.NameValueError()
            
        if is_email_address_valid(self.email):
            self.email = self.email.lower().lstrip().rstrip()
        else:
            raise me.EmailFormatError()

        if len(self.password) <= 20:
            if is_password_valid(self.password):
                self.password = self.password.rstrip().lstrip()
                self.password = make_password(self.password)
            else:
                raise me.InvalidPasswordError(self.password)                
        super(User, self).save(*args, **kwargs)

    """ class methods """
    @classmethod
    def get_user(cls, email: str, password: str) -> Union[User, None]:
        """ attempts to get a user using the provided email and password.

        if credentials match, User object is returned, else None."""

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
            else: 
                return None
        except:
            return None
        
    @classmethod
    def get_objects_alphabethical_order(cls) -> QuerySet:
        """method to objects in alphabethical order
        based on the value of their  field."""

        return User.objects.extra(
            select={"lower_name": "lower(name)"}).order_by("lower_name")
            