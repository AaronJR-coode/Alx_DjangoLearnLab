from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManage(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please set email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Your not staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Your not superuser')
        
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    date_of_birth = models.DateField(unique=True, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)

    objects = CustomUserManage()

    USERNAME_FIELD = 'date_of_birth'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    def __str__(self):
        return self.email
