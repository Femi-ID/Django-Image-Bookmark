from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

# In order to keep your code generic, use the get_user_model() method to retrieve the user model
# and the AUTH_USER_MODEL setting to refer to it when defining a model's relationship
# with the user model, instead of referring to the auth user model directly.
# You can read more information about this at
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.get_user_model.


"""
CUSTOM USER MODEL
Django also offers a way to substitute the whole user model with your own custom model.
Your user class should inherit from Django's AbstractUser class, which provides the full
implementation of the default user as an abstract model. You can read more about this method at
https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model.
"""
