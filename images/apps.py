from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'

    def ready(self):
        # import signal handlers
        from . import signals


#  * We're yet to makemigrations for images model*
# Open the shell with the python manage.py shell command and run the following code:
    # from images.models import Image
    # for image in Image.objects.all():
    # image.total_likes = image.users_like.count()
    # image.save()
