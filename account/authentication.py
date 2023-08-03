"""
An authentication backend is a class that provides the following two methods:
authenticate(), get_user(). Both has to return a user object if credentials valid.
Creating a custom authentication backend is as simple as writing a Python class that implements both methods.
You can read more information about customizing authentication at:
https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#otherauthentication-sources.
"""

from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """Authenticate users using an e-mail address."""
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

