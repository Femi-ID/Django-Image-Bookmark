from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
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


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Add following field to User dynamically by retrieving the user model by using the generic function get_user_model()
user_model = get_user_model()  # to monkey patch the User model, it's not a recommended way of adding fields to models.
user_model.add_to_class('following', models.ManyToManyField('self',
                                                            through=Contact,
                                                            related_name='followers',
                                                            symmetrical=False))

#  you refer to 'self' in the ManyToManyField field to create a relationship to the same model
# symmetrical=False: defines a non-symmetrical relatship (if I follow you, it doesn't mean that you automatically follow me).
# If you want to use your custom user model, take a look at the documentation at
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model.


